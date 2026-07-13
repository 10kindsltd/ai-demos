# Localization QA Toolkit

An AI-assisted quality toolkit for a translation agency. Human translators do the
translating; Claude runs the checks around them — on the **source copy before**
translation, on the **translated copy after**, and then turns the findings into a
client-ready **report**.

It is deliberately **client-agnostic**. None of the skills know Warden's (or any
client's) rules in advance. Each client's brand and terminology material lives in *that
client's* folder, and the skills discover and apply it at runtime. Add a new client by
dropping their guides in a folder — no skill changes required.

## The workflow

```
source copy ──▶ content-style-review ──▶ human translation ──▶ translation-consistency-check ──▶ qa-report
                (pre-translation check)     (done by people)      (post-translation drift check)   (dashboard + sign-off)
```

## The skills

All three live under [`.claude/skills/`](.claude/skills/) and load automatically.

| Skill | When it runs | What it does |
|---|---|---|
| [`content-style-review`](.claude/skills/content-style-review/SKILL.md) | On source copy, **before** translating | Grammar/mechanics, brand voice, and terminology check against the client's guides. Outputs a findings table. |
| [`translation-consistency-check`](.claude/skills/translation-consistency-check/SKILL.md) | On translated copy, **after** translating | Two reports: (1) per-translation compliance in each language, (2) cross-locale **drift** — terminology, register/formality, numeric claims, structure. |
| [`qa-report`](.claude/skills/qa-report/SKILL.md) | After either check | Turns the findings into a shareable **HTML dashboard** (severity heatmap + drill-down) and a branded **PDF sign-off** for the client (printed from HTML by a headless browser — no extra tools to install). |

Triggering is natural language — you don't type the skill name. "Check this blog post
before we translate it," "compare these translations for drift," or "turn that into a
report I can send the client" each pull in the right skill.

## The knowledge convention (how a client's rules get applied)

This is the important part, and the reason the skills are reusable. **Logic ships in the
skill; knowledge stays in the client's project.** A skill contains only *how* to review;
it discovers *what the rules are* every run by searching the current project.

**Where to put a client's material** — create a folder per client and drop their guides
in, in any format (`.md`, `.pdf`, …):

```
clients/<client-name>/
    <anything>-brand-guidelines.pdf
    <anything>-localization-style-guide.md
    <anything>-glossary.md
    ...
```

**What the skills look for** — a conventional folder (`clients/<name>/`, `references/`,
`style-guide/`, `brand/`), or any file whose name matches: `*brand*`, `*style*guide*`,
`*voice*`, `*tone*`, `*terminology*`, `*glossary*`, `*localization*`. The
consistency check additionally prioritizes anything with **per-locale** rules — a
term-handling table mapping English → per-language treatment, and formality/register
notes.

The live example is [`clients/warden/`](clients/warden/):

- [`warden-brand-guidelines.pdf`](clients/warden/warden-brand-guidelines.pdf) — voice,
  approved/banned terms, claims discipline, mechanics.
- [`warden-localization-style-guide.md`](clients/warden/warden-localization-style-guide.md)
  — the master term-handling table across 7 locales, per-locale formality rules, and
  transcreation guidance.

To onboard a second client, make `clients/acme/`, drop their guides in, and run the same
skills against their copy. Nothing else changes.

## Using it

**Pre-translation check** — the demo source copy is
[`test-blog-post.md`](test-blog-post.md) (Warden marketing copy with planted
violations):

> Check `test-blog-post.md` against Warden's brand guidelines before we send it to
> translation.

You'll get a findings table flagging the banned terms ("annihilated", "cyber-monsters"),
the overstated "100% protection" claim, the lowercase "warden", and the grammar slips.

**Post-translation check** — the demo translation set is
[`test-translations/`](test-translations/) (an English source plus French and German
translations, with drift planted in the French):

> Run a consistency check on the translations in `test-translations/` against the
> English source.

You'll get two reports. The drift report should catch that the French changed the CPU
figure to "moins de 5 %" (the source says under 2%), used "protection instantanée" in
the body where the heading says "protection en temps réel", and slipped into informal
"tu verras" where fr-FR defaults to *vous*.

**Report** — after either check:

> Turn that into a QA report I can send the client.

Produces the HTML dashboard and a branded PDF sign-off. The PDF is made by printing an
HTML report with a headless browser (Chrome/Brave/Edge), so there's nothing extra to
install. Both land in `qa-output/` at the project root (git-ignored) — that's the only
place this skill writes.

**More demo content** — [`demo-samples/`](demo-samples/) has a marketing-email sample
for the pre-check and a three-locale set (es-419, de-DE, fr-FR) for the post-check, each
with an answer key of the planted issues in [`demo-samples/README.md`](demo-samples/README.md).

## Testing

Both check skills ship eval suites with fixtures and answer keys under their `evals/`
folders — a planted-violation recall test and a clean false-positive control each:

- [`content-style-review/evals/`](.claude/skills/content-style-review/evals/)
- [`translation-consistency-check/evals/`](.claude/skills/translation-consistency-check/evals/)

Run them with the `skill-creator` skill (enabled in
[`.claude/settings.local.json`](.claude/settings.local.json)):

> Run the evals for the translation-consistency-check skill.

## Installing as a plugin (optional)

The `.claude/skills/` layout is already plugin-ready. To share one pinned copy of these
skills across every translator on the team, package them as a Claude Code plugin
(`claude plugin init`) and distribute via a marketplace. The knowledge convention above
is what makes this clean: translators install the skills once, and each client's rules
are still supplied per-project by dropping guides into `clients/<name>/` — so a glossary
update is just editing a file in that client's repo, never a plugin release.
