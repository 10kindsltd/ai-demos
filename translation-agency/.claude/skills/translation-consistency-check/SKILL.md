---
name: translation-consistency-check
description: Post-translation QA for a set of translated documents — checks each translation against the client's brand/style/terminology guides AND compares the translations against each other (and the source) for drift in terminology, register, numeric claims, and structure. Use this whenever the user has multiple translated versions of the same source content (different locales, or multiple translators/passes on one locale) and wants them reviewed before delivery — phrases like "compare these translations," "check consistency across locales," "post-translation review," or "did the translators drift from the term list." Produces two separate reports, not one combined table — don't merge them.
---

# Translation Consistency Check

Given a source document and one or more translated versions of it (or just several
translated versions with no source provided), produce two separate reports:

1. **Per-translation brand/style/terminology compliance** — does each translation, read
   on its own in its own language, follow the client's guides?
2. **Cross-translation drift analysis** — do the translations agree with each other
   (and with the source) on terminology, register, numbers, and structure?

These answer different questions and can disagree — a translation can be perfectly
consistent with the other locales while still violating the client's style guide, or
vice versa. Keep the two reports separate; don't fold drift findings into the compliance
table or vice versa.

## Step 1: Identify the inputs

Work out what you've been given:

- The **source document**, if provided — the report on drift is much stronger with it,
  since you can check translations against a shared original meaning rather than just
  against each other. If no source is given, proceed with cross-translation comparison
  alone and say so.
- Each **translated document**, with its locale/language. If locale isn't stated,
  identify it from the language of the text.

## Step 2: Find the client's reference material

Same approach as a general style review — look in the current project for anything that
reads like brand, voice, style, or terminology guidance (conventional folders like
`references/`, `style-guide/`, `brand/`, `clients/<name>/`; filenames like `*brand*`,
`*style*guide*`, `*terminology*`, `*glossary*`, `*localization*`). Read what you find in
full. For this skill, prioritize anything with **per-locale rules**: term-handling
tables that map an English term to per-language treatment, formality/register notes
(e.g. T–V forms, honorific tiers), and any locale-specific do's/don'ts. If nothing
locale-specific exists, use whatever general brand/style material you can find and note
in the report that locale-specific guidance wasn't available.

## Step 3: Report 1 — per-translation compliance

For each translated document, run it through the same kind of review as a general
content style check, applied in that document's own language: grammar/mechanics
appropriate to that language, brand voice/tone (does the translation read calm/urgent/
formal in the way the brand guide wants for that locale?), and terminology (does it use
the approved term for each locale per any term-handling table, and avoid anything the
locale notes flag, like wrong-register pronouns or banned loanword choices?).

Output one markdown table per translation (or one table with a locale column if there
are many short documents), ordered by position in that document:

| # | Location / quote | Issue | Category | Suggested fix | Reference |
|---|---|---|---|---|---|

Same column meanings as a standard style review: quote for findability, category is
Grammar / Voice-tone / Terminology, and reference cites the specific guide and
section. Findings with no guideline basis get "Standard grammar" as the reference.

## Step 4: Report 2 — cross-translation drift

This is the comparison the other report can't do: read the translations *against each
other* (and the source, if you have it) rather than each in isolation. Look for:

- **Terminology drift** — the same source term or concept rendered differently in
  different places. This includes the same term translated two different ways within
  one locale's document (internal inconsistency — a sign of multiple translators or
  passes), and cases where a term-handling table specifies one treatment but a
  translation does something else. Also check whether a term marked "keep in English"
  in the guide was actually translated in some locales but not others.
- **Register/formality drift** — inconsistent formality within a single translation
  (e.g. switching between formal and informal pronouns without reason), or a formality
  choice that doesn't match what the locale notes specify as default.
- **Numeric and claim drift** — any statistic, percentage, or specific claim that
  doesn't match exactly across the source and all translations. These should never
  shift in translation; flag every mismatch regardless of how minor it looks, since a
  softened or rounded number is a compliance issue, not just a style one.
- **Structural drift** — sections, headings, or claims present in the source or in one
  translation but missing or reordered in another, which often indicates a translator
  worked from an outdated source version or skipped content.

Output as a second markdown table, separate from Report 1:

| # | Source segment / concept | Locale(s) affected | What was found | Expected treatment | Reference |
|---|---|---|---|---|---|
| 1 | "under 2% CPU impact" | de-DE | Rendered as "geringe CPU-Auslastung" (vague "low CPU usage") | Exact figure must be preserved in every language | Brand guide, claims discipline |

- **Locale(s) affected**: name every locale where the drift shows up, not just one — if
  three of five translations agree and two don't, say which two.
- If a term-handling table exists, use it as the ground truth for "expected treatment."
  If no such table exists, use the source document's own treatment of the term/claim as
  the baseline instead.

## After both reports

Add a short combined summary (3-5 sentences): which locales came out cleanest, whether
compliance issues and drift issues cluster around the same passages (often a sign the
source itself was ambiguous, not that a translator erred), and whether anything found
should go to the client's query log / in-market reviewer process rather than being
silently corrected — translation guides often specify that legal-equivalence gaps or
judgment calls get flagged upstream, not fixed downstream.
