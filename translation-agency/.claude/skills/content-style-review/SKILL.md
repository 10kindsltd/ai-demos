---
name: content-style-review
description: Analyzes grammar, mechanics, brand voice, and terminology in a piece of text or a document, and outputs a table of findings with suggested fixes. Discovers and applies whatever brand/style/terminology guides exist in the current project — use this whenever the user shares client copy to proofread, asks for a grammar or style check, wants copy checked against a brand voice or banned-terms list, or is preparing content for translation/localization. Trigger even if the user just says "check this" or "does this sound right" about a piece of copy, as long as the project has (or might have) brand/style reference material to check it against.
---

# Content Style Review

Review text or a document for grammar/mechanics errors, brand-voice violations, and
terminology issues, then report findings as a table the reader can act on line by line.

This skill is intentionally generic — it doesn't know any one client's rules in
advance. Every client's brand and style guides live in *their* project, not in this
skill. Your first job on every run is to find them.

## Step 1: Find the reference material

Look in the current project for anything that reads like brand, voice, style, or
terminology guidance. Check, roughly in this order:

1. A conventional folder if one exists: `references/`, `style-guide/`, `brand/`,
   `clients/<name>/`, or similar.
2. Files anywhere in the project whose names suggest they're relevant: `*brand*`,
   `*style*guide*`, `*voice*`, `*tone*`, `*terminology*`, `*glossary*`,
   `*localization*`.
3. If the user's message names a client or points at a specific file/folder, start
   there instead of guessing.

Read whatever you find in full before reviewing — these documents are usually short
enough, and a rule or term-table row you skip is a finding you'll miss. If you find
nothing, say so before reviewing: proceed with a plain grammar/mechanics pass only, and
tell the user you found no brand/style material to check against (so they know the
review is partial, and can point you at the right file if one exists).

## Step 2: Understand what kind of guidance you found

Client guides vary in shape, but most brand/style documents cluster into a few kinds of
rules. As you read, sort what you find into these buckets (skip any that don't apply):

- **Mechanics** — punctuation, capitalization, numeral conventions, formatting rules
  (e.g. Oxford comma, sentence case vs. title case, em dash vs. semicolon).
- **Voice & tone** — the personality the brand wants (calm vs. urgent, formal vs.
  casual, jargon vs. plain language), often broken down by channel or content type.
- **Terminology** — approved vs. banned words/phrases, defined terms, product names and
  their capitalization, claims that must never be softened or overstated.
- **Localization** — how terms and content should be handled for translation: what
  stays in English, what gets transcreated vs. translated literally, per-locale
  formality or register rules. Only relevant if the text is explicitly for translation,
  names a target locale, or the user asks about localization.

## Step 3: Review the text

Work through the text making a pass for each bucket you identified in Step 2, plus
always a plain grammar pass (spelling, agreement, punctuation, run-ons, dangling
modifiers — this applies regardless of whether any client guide exists). Not every pass
will surface something in every document — only report real findings, and it's fine for
a pass to come back empty.

## Output format

Report findings as a single markdown table, ordered by their position in the source
text:

| # | Location / quote | Issue | Category | Suggested fix | Reference |
|---|---|---|---|---|---|
| 1 | "the AI destroyed the threat instantly" | Uses a banned term and implies AI when detection may be rules-based | Terminology | "we detected and blocked the threat" | brand-guidelines.pdf, approved/banned terms |

- **Location / quote**: a short exact quote so the reader can find it, not a line
  number (documents may not have stable line numbers).
- **Category**: Grammar, Voice/tone, Terminology, or Localization.
- **Reference**: cite the specific document and section/table that justifies the
  finding. If a finding is plain grammar with no guideline basis, write "Standard
  grammar" instead of forcing a citation.

After the table, add a short summary (2-4 sentences) noting any pattern worth the
author's attention — e.g. repeated fear-based phrasing, or a term used inconsistently —
rather than just listing isolated errors.
