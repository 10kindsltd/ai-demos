import json
import os
import urllib.parse

import boto3
from google import genai
from google.genai import types
from prompt import SYSTEM_PROMPT, USER_PROMPT
from schema import QuoteExtraction

s3 = boto3.client("s3")
gemini = genai.Client()

BUCKET = os.environ["BUCKET_NAME"]
MODEL_ID = "gemini-3.1-flash-lite"
CONFIDENCE_THRESHOLD = 0.5


def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

    print(f"Processing: s3://{bucket}/{key}")

    parts = key.split("/")
    if len(parts) < 4 or parts[0] != "clients":
        print(f"Skipping unexpected key format: {key}")
        return

    client_id = parts[1]
    filename = parts[-1]
    quote_name = filename.replace(".pdf", "")

    pdf_bytes = s3.get_object(Bucket=bucket, Key=key)["Body"].read()

    response = gemini.models.generate_content(
        model=MODEL_ID,
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            USER_PROMPT,
        ],
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_json_schema": QuoteExtraction.model_json_schema(),
        },
    )

    extracted_dict = json.loads(response.text)

    quote = QuoteExtraction(**extracted_dict)

    low_confidence = find_low_confidence_fields(extracted_dict, CONFIDENCE_THRESHOLD)
    if low_confidence:
        print(f"LOW CONFIDENCE FIELDS: {low_confidence}")

    output_key = f"clients/{client_id}/extracted/{quote_name}.json"
    output = {
        "extraction": extracted_dict,
        "low_confidence_fields": low_confidence,
        "source_key": key,
    }
    s3.put_object(
        Bucket=BUCKET,
        Key=output_key,
        Body=json.dumps(output, indent=2),
        ContentType="application/json",
    )
    print(f"Wrote extraction to s3://{BUCKET}/{output_key}")

    render_comparison(client_id)


def find_low_confidence_fields(d: dict, threshold: float, path: str = "") -> list[str]:
    """Recursively find all extracted fields with confidence below threshold."""
    low = []
    for k, v in d.items():
        current_path = f"{path}.{k}" if path else k
        if isinstance(v, dict):
            if "confidence" in v and v["confidence"] < threshold:
                low.append(f"{current_path} (confidence={v['confidence']})")
            else:
                low.extend(find_low_confidence_fields(v, threshold, current_path))
    return low


def render_comparison(client_id: str):
    """List all extracted JSONs for client and re-render comparison HTML."""
    prefix = f"clients/{client_id}/extracted/"
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)

    if "Contents" not in response:
        print("No extractions found yet.")
        return

    quotes = []
    for obj in response["Contents"]:
        if not obj["Key"].endswith(".json"):
            continue
        body = s3.get_object(Bucket=BUCKET, Key=obj["Key"])["Body"].read()
        quotes.append(json.loads(body))

    print(f"Rendering comparison for {len(quotes)} quote(s)")

    from renderer import render_html
    html = render_html(quotes, client_id)

    html_key = f"clients/{client_id}/comparison.html"
    s3.put_object(
        Bucket=BUCKET,
        Key=html_key,
        Body=html.encode("utf-8"),
        ContentType="text/html",
    )
    print(f"Wrote comparison to s3://{BUCKET}/{html_key}")
