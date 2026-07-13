# Answer key — warden-drift fixture (source-en.md + fr-FR.md + de-DE.md)

## Report 1 — per-translation compliance

### fr-FR — expected findings
| # | Quote (substring match ok) | Category | Notes |
|---|---|---|---|
| 1 | "La protection instantanée" | Terminology | Should be "protection en temps réel" (matches heading, term table) |
| 2 | "tableau de bord" | Terminology | fr-FR locale note: "Dashboard" should stay EN in tech contexts |
| 3 | "tu verras" | Voice/tone or Grammar | fr-FR defaults to vous; no casual-social context here |

### de-DE — expected findings
None. This document should come back clean on Report 1 (terminology, register, and tone all match the guide). A near-empty table here is correct, not a miss.

## Report 2 — cross-translation drift

| # | Source segment | Locale(s) affected | Notes |
|---|---|---|---|
| 1 | "under 2% average CPU impact" | fr-FR | Rendered as "moins de 5 %" — wrong number, not just softened. Highest-severity finding (claims discipline). |
| 2 | Closing paragraph ("If Warden Home blocks something...") | de-DE | Entirely missing from the translation — structural drift, not a wording issue. |
| 3 | Formality register (vous default) | fr-FR | "tu verras" breaks an otherwise consistent vous register within the same document — internal inconsistency. |
| 4 | "Real-time protection" term | fr-FR | Heading uses "protection en temps réel," body uses "protection instantanée" — internal drift. de-DE uses "Echtzeitschutz" consistently and should be named as the contrast case. |

## Assertion summary
- Report 1: fr-FR table has 3 rows matching the above; de-DE table is empty or has no more than 1 minor extra finding.
- Report 2: has 4 rows matching the above, each naming the correct affected locale(s).
- Structural: output contains two clearly separate reports/tables, not one merged table.
- The CPU number finding must be present in Report 2 in some form — this is the highest-stakes single check (real financial/legal-adjacent claim accuracy).
