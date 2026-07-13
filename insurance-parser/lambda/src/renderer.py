"""
Renders the comparison HTML from extracted quote JSONs.
Pure deterministic Python — no LLM involved here.
"""

from __future__ import annotations

import html
from datetime import datetime

CONFIDENCE_THRESHOLD = 0.5

# Field-path substrings whose values should render as GBP currency
CURRENCY_HINTS = ["sum_insured", "limit", "gross", "net", "ipt", "money", "transit", "excess"]

# Field-path substrings that hold dates
DATE_HINTS = ["date", "valid_until", "period_start", "period_end"]

# Date formats the model might emit, normalised to YYYY-MM-DD
_DATE_FORMATS = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%d %B %Y", "%d %b %Y"]


def _normalise_date(s: str) -> str:
    """Parse a date string into YYYY-MM-DD; return unchanged if not a recognised date."""
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return s  # e.g. "14 days from issue"


def _as_number(v) -> float | None:
    """Coerce a value to a number, stripping currency symbols and separators."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        cleaned = v.replace(",", "").replace("£", "").replace("$", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None

# Fields to show in the comparison grid, in display order
# (label, dot-path into extraction dict)
COMPARISON_ROWS = [
    # Premium (headline)
    ("Gross Premium", "premium.gross"),
    ("Net Premium", "premium.net"),
    ("IPT", "premium.ipt"),
    ("Instalments", "premium.instalments_available"),
    # Quote meta
    ("Quote Reference", "quote_reference"),
    ("Valid Until", "quote_valid_until"),
    # Property
    ("Buildings Sum Insured", "property.buildings_sum_insured"),
    ("Contents & Machinery", "property.contents_machinery_sum_insured"),
    ("Stock Sum Insured", "property.stock_sum_insured"),
    ("Property Excess", "property.excess"),
    ("Perils Included", "property.perils_included"),
    ("Perils Excluded", "property.perils_excluded"),
    # BI
    ("BI Gross Profit", "business_interruption.gross_profit_sum_insured"),
    ("BI Indemnity Period", "business_interruption.indemnity_period_months"),
    ("BI Excess", "business_interruption.excess"),
    # Liability
    ("Employers Liability", "liability.employers_liability_limit"),
    ("Public / Products Liability", "liability.public_liability_limit"),
    ("Liability Excess", "liability.excess"),
    # Other
    ("Money Limit", "other_covers.money_limit"),
    ("Goods in Transit", "other_covers.goods_in_transit_limit"),
]

# Fields where a LOWER value vs others is a flag worth calling out
FLAG_LOWER = {
    "premium.gross",
    "property.contents_machinery_sum_insured",
    "business_interruption.gross_profit_sum_insured",
    "business_interruption.indemnity_period_months",
    "liability.public_liability_limit",
    "other_covers.money_limit",
    "other_covers.goods_in_transit_limit",
}

# Fields where a HIGHER value is a flag (e.g. excess — higher = worse for insured)
FLAG_HIGHER = {
    "property.excess",
    "business_interruption.excess",
    "liability.excess",
}


def get_nested(d: dict, path: str):
    """Resolve dot-path from extraction dict. Returns ExtractedValue dict or None."""
    parts = path.split(".")
    current = d.get("extraction", d)
    for part in parts:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def fmt_value(field_path: str, ev: dict | None) -> str:
    """Format an ExtractedValue for display."""
    if ev is None or ev.get("value") is None:
        return "—"
    v = ev["value"]
    if isinstance(v, list):
        return ", ".join(str(x) for x in v) if v else "—"
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if any(x in field_path for x in DATE_HINTS):
        return _normalise_date(str(v))
    if "rate" in field_path:
        return f"{v}%"
    if "months" in field_path:
        return f"{v} months"
    if any(x in field_path for x in CURRENCY_HINTS):
        num = _as_number(v)
        if num is not None:
            return f"£{num:,.0f}"
    return str(v)


def detect_flags(quotes: list[dict]) -> list[str]:
    """Generate plain-English flag strings by comparing extracted values across quotes."""
    flags = []
    if len(quotes) < 2:
        return flags

    # Sort by gross premium ascending (cheapest first)
    def gross(q):
        ev = get_nested(q, "premium.gross")
        num = _as_number(ev["value"]) if ev and ev.get("value") is not None else None
        return num if num is not None else float("inf")

    sorted_quotes = sorted(quotes, key=gross)
    cheapest = sorted_quotes[0]
    cheapest_name = get_nested(cheapest, "insurer_name")
    cheapest_label = cheapest_name["value"] if cheapest_name else "Cheapest quote"

    others = sorted_quotes[1:]

    for path in FLAG_LOWER:
        cheapest_ev = get_nested(cheapest, path)
        if cheapest_ev is None or cheapest_ev.get("value") is None:
            continue
        cheapest_val = cheapest_ev["value"]
        if not isinstance(cheapest_val, (int, float)):
            continue
        other_vals = []
        for q in others:
            ev = get_nested(q, path)
            if ev and isinstance(ev.get("value"), (int, float)):
                other_vals.append(ev["value"])
        if not other_vals:
            continue
        max_other = max(other_vals)
        if cheapest_val < max_other:
            label = next((r[0] for r in COMPARISON_ROWS if r[1] == path), path)
            flags.append(
                f"<strong>{label}:</strong> {cheapest_label} shows {fmt_value(path, cheapest_ev)} "
                f"vs {fmt_value(path, {'value': max_other})} elsewhere."
            )

    for path in FLAG_HIGHER:
        cheapest_ev = get_nested(cheapest, path)
        if cheapest_ev is None or cheapest_ev.get("value") is None:
            continue
        cheapest_val = cheapest_ev["value"]
        if not isinstance(cheapest_val, (int, float)):
            continue
        other_vals = []
        for q in others:
            ev = get_nested(q, path)
            if ev and isinstance(ev.get("value"), (int, float)):
                other_vals.append(ev["value"])
        if not other_vals:
            continue
        min_other = min(other_vals)
        if cheapest_val > min_other:
            label = next((r[0] for r in COMPARISON_ROWS if r[1] == path), path)
            flags.append(
                f"<strong>{label}:</strong> {cheapest_label} carries a higher excess "
                f"({fmt_value(path, cheapest_ev)} vs {fmt_value(path, {'value': min_other})})."
            )

    # Perils excluded check
    cheapest_excl_ev = get_nested(cheapest, "property.perils_excluded")
    if cheapest_excl_ev and cheapest_excl_ev.get("value"):
        excl = cheapest_excl_ev["value"]
        if isinstance(excl, list) and excl:
            flags.append(
                f"<strong>Perils excluded by {cheapest_label}:</strong> {', '.join(excl)}. "
                f"Check whether other quotes include these."
            )

    # Warranties check
    cheapest_warranties = cheapest.get("extraction", cheapest).get("warranties", [])
    if cheapest_warranties:
        flags.append(
            f"<strong>Warranties ({cheapest_label}):</strong> {'; '.join(cheapest_warranties)}. "
            f"Breach may void cover."
        )

    # Subjectivities check
    cheapest_subs = cheapest.get("extraction", cheapest).get("subjectivities", [])
    if cheapest_subs:
        sub_texts = "; ".join(s.get("text", "") for s in cheapest_subs)
        flags.append(
            f"<strong>Outstanding subjectivities ({cheapest_label}):</strong> {sub_texts}. "
            f"Quote not yet firm."
        )

    # Quote validity check
    valid_ev = get_nested(cheapest, "quote_valid_until")
    if valid_ev and valid_ev.get("raw_text") and "14" in str(valid_ev.get("raw_text", "")):
        flags.append(
            f"<strong>Short validity ({cheapest_label}):</strong> Quote open 14 days only."
        )

    return flags


def render_html(quotes: list[dict], client_id: str) -> str:
    """Render the full comparison HTML page."""

    # Sort cheapest first
    def gross(q):
        ev = get_nested(q, "premium.gross")
        num = _as_number(ev["value"]) if ev and ev.get("value") is not None else None
        return num if num is not None else float("inf")

    quotes_sorted = sorted(quotes, key=gross)

    insurer_names = []
    for q in quotes_sorted:
        ev = get_nested(q, "insurer_name")
        insurer_names.append(ev["value"] if ev and ev.get("value") else "Unknown")

    flags = detect_flags(quotes_sorted)

    # Build table rows
    rows_html = ""
    for label, path in COMPARISON_ROWS:
        cells = f'<td class="row-label">{label}</td>'
        values = []
        evs = []
        for q in quotes_sorted:
            ev = get_nested(q, path)
            evs.append(ev)
            values.append(ev["value"] if ev and ev.get("value") is not None else None)

        for i, (q, ev) in enumerate(zip(quotes_sorted, evs)):
            display = fmt_value(path, ev)
            low_conf = ev and ev.get("confidence", 1.0) < CONFIDENCE_THRESHOLD
            not_found = ev is None or ev.get("value") is None

            css = "cell"
            title = ""
            if low_conf:
                css += " low-confidence"
                conf = ev.get("confidence", 0)
                raw = html.escape(str(ev.get("raw_text", "") or ""), quote=True)
                title = f' title="Low confidence: {conf:.2f} — review recommended. Raw: {raw}"'
            elif not_found:
                css += " not-found"

            # Highlight if this is the min/max among numeric values (for flag paths)
            numeric_vals = [v for v in values if isinstance(v, (int, float))]
            if isinstance(values[i], (int, float)) and len(numeric_vals) > 1:
                if path in FLAG_LOWER and values[i] == min(numeric_vals) and min(numeric_vals) < max(numeric_vals):
                    css += " flag-low"
                elif path in FLAG_HIGHER and values[i] == max(numeric_vals) and min(numeric_vals) < max(numeric_vals):
                    css += " flag-high"

            cells += f'<td class="{css}"{title}>{display}</td>'

        rows_html += f"<tr>{cells}</tr>\n"

    # Headers
    header_cells = '<th class="row-label">Field</th>'
    for i, name in enumerate(insurer_names):
        ev = get_nested(quotes_sorted[i], "premium.gross")
        gross_display = fmt_value("premium.gross", ev)
        header_cells += f'<th><div class="insurer-name">{name}</div><div class="insurer-premium">{gross_display}</div></th>'

    # Flags section
    flags_html = ""
    if flags and len(quotes_sorted) > 1:
        flag_items = "".join(f"<li>{f}</li>" for f in flags)
        cheapest_ev = get_nested(quotes_sorted[0], "insurer_name")
        cheapest_name = cheapest_ev["value"] if cheapest_ev else "Cheapest quote"
        flags_html = f"""
        <div class="flags">
            <h2>⚠️ Cheapest is not necessarily best cover</h2>
            <p>The following differences were detected for <strong>{cheapest_name}</strong> (cheapest quote):</p>
            <ul>{flag_items}</ul>
            <p class="disclaimer">This comparison is generated automatically. The broker should verify all details before making recommendations.</p>
        </div>
        """

    waiting_html = ""
    # if len(quotes_sorted) == 1:
    #     waiting_html = '<div class="waiting">⏳ Waiting for more quotes — comparison will update automatically as they arrive.</div>'
    # elif len(quotes_sorted) == 2:
    #     waiting_html = '<div class="waiting">⏳ 2 of 3 quotes received — comparison will update when the third arrives.</div>'

    insured_ev = get_nested(quotes_sorted[0], "insured_name") if quotes_sorted else None
    insured_name = insured_ev["value"] if insured_ev and insured_ev.get("value") else client_id

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quote Comparison — {insured_name}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f6fa; color: #222; }}
  .page {{ max-width: 1100px; margin: 0 auto; padding: 32px 24px; }}
  header {{ margin-bottom: 28px; }}
  header h1 {{ font-size: 1.6rem; font-weight: 700; color: #1a1a2e; }}
  header p {{ color: #666; margin-top: 4px; font-size: 0.9rem; }}
  .waiting {{ background: #fff8e1; border-left: 4px solid #f9a825; padding: 14px 18px; border-radius: 4px; margin-bottom: 24px; font-size: 0.95rem; }}
  .flags {{ background: #fff3f3; border-left: 4px solid #e53935; padding: 20px 24px; border-radius: 6px; margin-bottom: 28px; }}
  .flags h2 {{ font-size: 1.05rem; color: #b71c1c; margin-bottom: 10px; }}
  .flags ul {{ padding-left: 20px; }}
  .flags li {{ margin-bottom: 8px; font-size: 0.92rem; line-height: 1.5; }}
  .flags p {{ font-size: 0.9rem; color: #555; margin-top: 10px; }}
  .disclaimer {{ font-style: italic; color: #888 !important; font-size: 0.82rem !important; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
  th {{ background: #1a1a2e; color: white; padding: 14px 16px; text-align: left; }}
  th.row-label {{ width: 220px; background: #12122a; }}
  .insurer-name {{ font-size: 1rem; font-weight: 600; }}
  .insurer-premium {{ font-size: 0.82rem; color: #aab; margin-top: 2px; }}
  td {{ padding: 11px 16px; font-size: 0.9rem; border-bottom: 1px solid #eee; vertical-align: top; }}
  td.row-label {{ font-weight: 500; color: #444; background: #fafafa; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f0f4ff; }}
  tr:hover td.row-label {{ background: #e8edf8; }}
  .flag-low {{ background: #fff3cd !important; font-weight: 600; color: #856404; }}
  .flag-high {{ background: #fde8e8 !important; font-weight: 600; color: #842029; }}
  .low-confidence {{ /*border-bottom: 2px dashed #f9a825; cursor: help;*/ }}
  .not-found {{ color: #bbb; }}
  .legend {{ margin-top: 20px; display: flex; gap: 20px; flex-wrap: wrap; font-size: 0.8rem; color: #666; }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .swatch {{ width: 14px; height: 14px; border-radius: 2px; }}
</style>
</head>
<body>
<div class="page">
  <header>
    <h1>Quote Comparison — {insured_name}</h1>
    <p>Commercial Combined Renewal · {len(quotes_sorted)} quote(s) received · Sorted cheapest to dearest</p>
  </header>
  {waiting_html}
  {flags_html}
  <div class="table-wrap">
    <table>
      <thead><tr>{header_cells}</tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
  <div class="legend">
    <div class="legend-item"><div class="swatch" style="background:#fff3cd;border:1px solid #e6c200"></div> Lower than other quotes</div>
    <div class="legend-item"><div class="swatch" style="background:#fde8e8;border:1px solid #e53935"></div> Higher excess than other quotes</div>
    <div class="legend-item"><div class="swatch" style="border-bottom:2px dashed #f9a825;border-top:1px solid #eee;border-left:1px solid #eee;border-right:1px solid #eee"></div> Low confidence — hover for detail</div>
  </div>
</div>
</body>
</html>"""
