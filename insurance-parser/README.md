# Quote Comparison Pipeline

Drops insurance quote PDFs into S3 → extracts structured data via Claude → renders a comparison HTML that updates as each quote arrives.

## Prerequisites

- AWS CLI configured (`aws configure`)
- SAM CLI (`brew install aws-sam-cli`)
- Python 3.12
- An existing S3 bucket

## Deploy/Destroy

```bash
just login
just deploy
just destroy
```

After deploying, configure an S3 event notification on your bucket to invoke the `ExtractorFunction` ARN (shown in stack outputs) on `s3:ObjectCreated:*` events with prefix `clients/` and suffix `.pdf`.

## Usage

Drop PDFs into your bucket under `clients/{client-id}/quotes/`:

```bash
BUCKET=your-bucket-name

# Upload quotes one at a time — HTML updates after each
cd demo-data
aws s3 cp Quote_A_Aldgate.pdf s3://$BUCKET/clients/brindle-hart/quotes/
aws s3 cp Quote_B_Pennine.pdf s3://$BUCKET/clients/brindle-hart/quotes/
aws s3 cp Quote_C_Vantage.pdf s3://$BUCKET/clients/brindle-hart/quotes/

# Download and open the comparison
aws s3 cp s3://$BUCKET/clients/brindle-hart/comparison.html ./comparison.html
open comparison.html
```

## S3 folder structure

```
quote-pipeline-{account-id}/
  clients/
    brindle-hart/
      quotes/          ← drop PDFs here
      extracted/       ← written by Lambda (JSON per quote)
        aldgate.json
        pennine.json
        vantage.json
      comparison.html  ← re-rendered after every upload
```

## Local testing

```bash
# Invoke locally with a mock S3 event
sam local invoke ExtractorFunction --event events/test_event.json
```

Example `events/test_event.json`:
```json
{
  "Records": [{
    "s3": {
      "bucket": {"name": "quote-pipeline-123456789012"},
      "object": {"key": "clients/brindle-hart/quotes/aldgate.pdf"}
    }
  }]
}
```

## Tuning

- **Confidence threshold**: change `CONFIDENCE_THRESHOLD` in `handler.py` and `renderer.py`
- --**Synonym mapping**: extend the table in `prompt.py` → `SYSTEM_PROMPT`--
- **Flag rules**: add paths to `FLAG_LOWER` / `FLAG_HIGHER` in `renderer.py`
- **Model**: change `MODEL_ID` in `handler.py`
