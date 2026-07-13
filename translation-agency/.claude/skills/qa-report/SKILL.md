---
name: qa-report
description: Turns the findings from a content-style-review or translation-consistency-check into a client-ready QA deliverable — a self-contained HTML dashboard with a severity heatmap across locales plus a branded PDF sign-off document produced by printing HTML with a headless browser (no external tools to install). Use this after running either check when the user wants to package the findings for the client: "make a QA report," "turn this into a dashboard," "give me something I can send the client," "visualize the drift report," "export the findings." Works from findings already produced in the conversation; if none exist yet, run the appropriate check first.
---

# QA Report

Package review findings into two client-facing deliverables:

1. **An HTML dashboard** — a severity heatmap (finding categories × locales) plus a
   filterable findings list. This is the at-a-glance view for a screen or a shared link.
2. **A branded PDF sign-off** — a print-styled document the agency can attach to a delivery.

This skill doesn't review copy itself. It consumes findings that
`content-style-review` (pre-translation) or `translation-consistency-check`
(post-translation) already produced. Like those skills it is **client-agnostic** — it
carries no client's rules, and picks up branding for the document from whatever guide is
discoverable in the project.

## Step 1: Gather the findings and run metadata

Use the findings already in the conversation. If there are none — the user asked for a
report without running a check first — run the appropriate check now (a single source
document → `content-style-review`; a source plus translations, or several translations →
`translation-consistency-check`), then continue.

Pull together the metadata the deliverables need:

- **client** — the client whose guides were used (e.g. discovered under `clients/<name>/`).
- **source** — the document under review (title or filename).
- **phase** — `pre-translation` (a `content-style-review` run) or `post-translation`
  (a `translation-consistency-check` run).
- **locales** — the locale codes reviewed. For a pre-translation check of one document,
  leave this empty.
- **date** — today's date.

Then normalize each finding into this shape (the dashboard and the document both use it):

| field | meaning |
|---|---|
| `locale` | locale code, or `source` for a pre-translation finding |
| `category` | one of Grammar, Voice/tone, Terminology, Register/formality, Numeric/claim, Structural |
| `severity` | `high`, `medium`, or `low` (see guidance below) |
| `report` | `compliance` (per-translation / style finding) or `drift` (cross-locale finding) |
| `quote` | short exact quote so the reader can locate it |
| `issue` | what's wrong |
| `fix` | suggested correction |
| `reference` | the guide + section that justifies it, or "Standard grammar" |

**Severity guidance** — be consistent, since it drives the heatmap colors and the verdict:

- **high** — anything that changes meaning or breaks a hard rule: numeric/claim drift (a
  changed or softened statistic), overstated claims the brand bans ("100% protection"),
  banned terms, register violations that flip formality in product/legal copy.
- **medium** — terminology drift or internal inconsistency, structural drift (missing or
  reordered content), voice/tone that's off-brand without being a false claim.
- **low** — minor mechanics, or a term preference with low risk of confusion.

**Overall verdict** — `fail` if any high-severity finding exists, `warn` if only
medium/low, `pass` if clean.

## Step 2: Build the HTML dashboard

Before writing any page markup, load the **artifact-design** skill (for layout and
theming) and the **dataviz** skill (the heatmap is a small sequential-severity map — keep
its colors accessible in both light and dark).

Start from [`references/dashboard-template.html`](references/dashboard-template.html). It
is fully self-contained (inline CSS/JS, no external assets) and renders the header,
heatmap, filters, and findings from a single JSON block. **You only replace the data** —
swap the JSON inside `<script id="qa-data">` for the real run (schema and a worked
example are in the file). Don't rewrite the CSS or JS unless the user asks for a design
change.

**Always write the file to `qa-output/` at the project root** (create the folder if it
doesn't exist), named after the source document — e.g.
`qa-output/<source-slug>-dashboard.html`. Every generated file this skill produces goes
in `qa-output/` and nowhere else, so the deliverables stay in one predictable, git-ignored
place. Open it in a browser to view; it's self-contained and works offline.

Optionally, for a shareable link, *also* publish it via the Artifact tool (the Artifact
wrapper supplies the `<!doctype>`/`<head>`/`<body>`, so pass only the inner content — the
`<style>` block, the page markup, and the two `<script>` blocks — not the template's outer
`<html>` shell). The local `qa-output/` copy is still written either way.

## Step 3: Build the client-facing PDF sign-off

The sign-off is a PDF, produced by **printing an HTML report with a headless
Chromium-based browser** — no Python, no pip, nothing for a non-technical user to
install beyond a browser they almost certainly already have. Don't reach for the
`pdf`/`docx` skills here; they need Python libraries and defeat the point.

Start from [`references/report-template.html`](references/report-template.html). It's a
print-styled, self-contained document that renders from the **same `qa-data` JSON schema
as the dashboard**, plus one extra field: a `summary` string. As with the dashboard, you
only replace the JSON — the template lays out the title block, the summary, a Report 1
(compliance) table, a "clean locales" note, a Report 2 (drift) table, and a sign-off
line. It splits findings into the two tables by their `report` field, so keep that field
right on every finding.

Write the `summary` in the **client's brand voice** — discover their guide the same way
the check skills do (`clients/<name>/`, or files matching `*brand*`, `*style*guide*`,
`*voice*`), and follow it. For Warden that means calm and plain-spoken, no alarmist
framing — a report about problems shouldn't itself sound alarmist.

Then fill and print — **both the filled HTML and the PDF go in `qa-output/`** at the
project root (same folder as the dashboard; create it if needed):

1. Save the filled template as `qa-output/<source-slug>-qa-report.html`.
2. Find a browser binary that exists — try, in order, Google Chrome, Brave, Microsoft
   Edge, Chromium (on macOS these live under `/Applications/<Name>.app/Contents/MacOS/`).
3. Print to PDF, writing into `qa-output/` (all Chromium browsers accept these flags):

   ```
   "<browser binary>" --headless=new --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="<abs path>/qa-output/<source-slug>-qa-report.pdf" \
     "file://<abs path>/qa-output/<source-slug>-qa-report.html"
   ```

4. Confirm the PDF was written. If no Chromium-based browser is found, say so and offer
   to open the HTML report in a browser so the user can print it manually — don't fall
   back to installing Python packages.

## Keep it client-agnostic

Nothing here is Warden-specific. Use whatever client, findings, and branding are in play,
and discover reference material at runtime — never hardcode a client's rules into the
report.
