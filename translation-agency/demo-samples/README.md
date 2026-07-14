# Demo samples

Extra content for demoing the toolkit, beyond the top-level `test-blog-post.md` and
`test-translations/`. Every sample has issues planted on purpose that map to Warden's
guides under [`../clients/warden/`](../clients/warden/), so you can run a skill live and
confirm it catches them. This file is the presenter's answer key — what *should* surface.

---

## 1. Pre-translation check — `email-newsletter.md`

A Warden monthly-summary email. **This is the point of the sample: it reads like a
perfectly normal, professional email.** Nothing jumps out to a casual reader — no
shouting, no obvious hype. Every violation is one you only catch if you've actually read
the brand guide, which is exactly what the skill is for. Run:

> Check demo-samples/email-newsletter.md against Warden's brand guidelines.

`content-style-review` should flag roughly these (≈12):

| What | Why | Guide |
|---|---|---|
| "our AI spotted it" | Say "we detected" — don't attribute detection to AI | Brand: approved terms |
| "…email attachment; our AI…" | Em dash preferred over semicolon | Brand: mechanics |
| "downloads, email attachments and USB drives" | Missing Oxford comma | Brand: mechanics |
| "less alerts than in May" | Should be "fewer alerts" (count noun) | Standard grammar |
| "impact on your system stayed under 2%" | **Restated proof point.** The approved claim is "under 2% average CPU impact during scans" — *exactly as written*. "System impact" broadens CPU to the whole machine, and "stayed under 2%" for a full month turns a lab average into a personal-telemetry claim. Restated → no longer pre-substantiated → needs a source/date footnote, or a rewrite back to the approved wording | Brand: proof points (§5), legal notes (§9) |
| "Attacks … have climbed sharply this year" | Unsourced claim, and nudges toward alarm — voice is calm | Brand: voice, legal notes |
| "blocks 99.8% of known malware" | **The key finding.** Not the approved figure (**99.7%**), so it is *not* pre-substantiated — which means it also needs a source/date footnote, and has none | Brand: proof points (§5), legal notes (§9) |
| "you can stop worrying about what lands in your inbox" | Soft absolute — edges into "guaranteed safe" | Brand: claims discipline |
| "up to fifty devices" | Numerals for all numbers → "50" | Brand: mechanics |
| "a Firewall" / "a central Dashboard" | Generic terms stay lowercase; only "Warden" is capitalized | Brand: mechanics |
| "Run a full sweep" | Use "scan", not "sweep" | Brand: approved terms |
| "let warden take care of it" | "Warden" is always capitalized | Brand: mechanics |

**Deliberately correct — the skill should NOT flag these** (this is the precision half of
the demo):

- "removed 3 threats" — the §6 table governs word choice, not exact sentences: "removed"
  and "threat" are the approved words, used correctly. (Contrast §5, which *is* an
  exactly-as-written rule — but only for proof-point claims.)
- Sentence-cased subject line and heading.
- The Oxford comma *is* present in "protects…, adds…, and gives…".
- "Real-time protection" — the correct product term.

> **The two stats are the heart of the test.** Both are bare — no footnote — and both are
> findings, but for *different reasons*, and a good review tells them apart:
>
> - **"under 2%"** — the approved *number*, but not the approved *claim*. §5
>   pre-substantiates "under 2% average CPU impact during scans" exactly as written; the
>   email broadens it to whole-system impact and a full-month personal claim. Fix: restore
>   the approved wording (or cite the actual telemetry).
> - **"99.8%"** — not the approved figure at all (it's 99.7%). Wrong number *and* uncited.
>   Fix: correct to the approved claim.
>
> A model that flags both as one generic "percentage with no footnote" issue has missed
> the distinction; a model that flags neither has missed §5 entirely. The expected output
> names one as drift from an approved claim and the other as an unapproved figure.

---

## 2. Post-translation check — `plan-comparison/`

A new source ("Choosing your Warden plan") plus **three** locales — **es-419, de-DE,
fr-FR** — so the check exercises the term table and locale notes across more than two
languages. Run:

> Run a consistency check on the translations in demo-samples/plan-comparison/ against
> the English source.

Expect **two separate reports**.

**Report 1 — per-translation compliance**

- **es-419** — three findings:
  - Mixes *usted* (title "su plan") with *tú* (body "puedes… tu…"); es-419 default is
    *usted* (§5).
  - "secuestro de datos" — *ransomware* stays in English for es (§3 term table).
  - "tablero" — es-419 uses *panel* for product UI (§5).
- **de-DE** — clean (correct *Echtzeitschutz*, *Firewall*, *Ransomware*, *Dashboard*,
  *Sie*, figure preserved).
- **fr-FR** — one finding: "tableau de bord" should stay *Dashboard* in fr tech
  contexts (§3, §5).

**Report 2 — cross-translation drift**

- **Numeric (high)** — price is $4.99 in the source, de-DE, and fr-FR, but **$5.99 in
  es-419**.
- **Terminology (keep-EN)** — *ransomware* kept in English in fr/de but translated to
  "secuestro de datos" in es-419.
- **Terminology (dashboard)** — three different treatments: *Dashboard* (de, correct),
  *tableau de bord* (fr), *tablero* (es).
- **Register** — es-419 switches between *usted* and *tú*.
- **Structural** — de-DE is missing the final "cancel any time" paragraph.

Cleanest locale: **de-DE** (only the structural miss). The **es-419 price change** is the
high-severity claims issue.

**Then package it:**

> Turn that into a QA report.

The dashboard heatmap should light up es-419 across Terminology / Register / Numeric,
fr-FR on Terminology, and de-DE on Structural only — and both the dashboard and the PDF
land in `../qa-output/`.
