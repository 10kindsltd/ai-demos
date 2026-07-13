# Warden Security — Multilingual Localization Style Guide

**Purpose:** This document guides translators and reviewers on *how* to localize Warden content — not just what words to use, but which decisions require judgment: when to keep English, when to translate literally, and when to transcreate. It applies across four content categories: **Product UI**, **Legal/Contract**, **Marketing**, and **Support/Help Center**, for the following locales:

| Code | Locale | Script | Formality system | Notes |
|---|---|---|---|---|
| fr-FR | French (France) | Latin | T–V (tu/vous) | Vous default in all categories except in-app tips |
| de-DE | German (Germany) | Latin | T–V (du/Sie) | Sie default; du only in casual social copy |
| es-419 | Spanish (Latin America) | Latin | T–V (tú/usted) | Usted default; regional neutrality required (no Spain-only slang) |
| pt-BR | Portuguese (Brazil) | Latin | Você-based | Less rigid T–V than European Portuguese; "você" reads neutral-friendly |
| ja-JP | Japanese | Kanji/Kana | Keigo (honorific tiers) | Teineigo (polite form) default; avoid excessive keigo in UI (reads stiff) |
| zh-CN | Chinese (Simplified) | Hanzi | No grammatical formality, but register matters | Avoid Traditional-only characters; state-sensitive terminology review required |
| ar-SA | Arabic (MSA) | Arabic, RTL | Formal register (fusha) default | RTL layout implications for UI; avoid regional dialect |

---

## 1. General Principles (apply to all locales unless overridden below)

1. **Default to translating.** English-as-default is the exception, not the rule — it exists to prevent *worse* outcomes (confusion, sounding try-hard, breaking brand recognition), not as a shortcut.
2. **Leave in English when:**
   - The term is a de facto global standard the target audience already uses in English more than in translation (e.g., "firewall," "ransomware" in many markets — see §3).
   - It's a proper noun / product name (Warden, Warden Home, Warden Business).
   - Translating it would require inventing an awkward neologism that native speakers don't actually use in daily speech (test: would a native IT professional say the translated term out loud, or say the English term?).
3. **Translate literally when** the source is functional/instructional and a literal translation reads naturally (most UI microcopy, most support docs).
4. **Transcreate when** the source relies on wordplay, rhythm, or cultural reference that won't survive literal translation (taglines, headlines, ad copy). Transcreation briefs are provided per-asset; translators should not transcreate silently without one.
5. **Never transcreate legal/contract content.** Legal text is translated for precision and terminological consistency with local law, never for tone. Flag — don't improvise — if a legal term has no clean equivalent.
6. **When in doubt, don't guess — flag it.** Use the query log (§7) rather than silently choosing an option.

---

## 2. Category-by-Category Guidance

### 2.1 Product UI (buttons, menus, in-app notifications)

- Prioritize brevity over completeness — UI space is constrained; a shorter, slightly less literal translation that fits the button is preferred over a precise but truncated one.
- Keep tone consistent with the English source's calm, factual voice (see brand style guide) — do not "warm up" UI text just because a locale is typically more informal in daily life; product UI stays neutral-polite across all locales.
- Threat notifications must remain short and factual in every language — resist the urge to soften or dramatize even where local norms might favor either.

### 2.2 Legal / Contract (EULA, privacy policy, terms of service)

- Use each jurisdiction's standard legal register, not a translation of English legal register. E.g., German contracts should read like German contracts, not like a German version of American legalese.
- Defined terms (capitalized terms like "Service," "Subscription," "User Data") must map to one, and only one, term per language throughout the entire document. Build a per-document defined-terms table before translating.
- Do not localize currency, jurisdiction, or governing-law clauses without explicit instruction — these are legally load-bearing and set per contract, not per translator discretion.
- If a concept has no direct legal equivalent in the target jurisdiction (e.g., certain U.S. arbitration clauses), flag to legal review rather than approximating.

### 2.3 Marketing (ads, landing pages, taglines)

- Taglines are transcreated, not translated (see §4 for the "Stay Warded" example across locales).
- Benefit-led claims must preserve the *specific* claim, not just the sentiment — "under 2% CPU impact" must stay a real, checkable number in every language, never softened into a vaguer phrase for smoother copy.
- Humor and wordplay: only attempt if a transcreation brief explicitly invites it. Default is confident-but-plain, per brand voice.

### 2.4 Support / Help Center

- Optimize for searchability in the target language: use the terms real users search for locally, even if a more "correct" technical term exists. Include the common term at least once even if the formal term is used as the primary heading.
- Step-by-step instructions: literal, numbered, no rhetorical flourishes.

---

## 3. Master Term Handling Table

Legend: **EN** = keep in English · **TR** = translate · **TR\*** = translate, but see locale note

| English term | fr-FR | de-DE | es-419 | pt-BR | ja-JP | zh-CN | ar-SA |
|---|---|---|---|---|---|---|---|
| Firewall | EN (*pare-feu* understood but EN dominant in tech contexts) | TR — *Firewall* (loanword, standard) | TR — *cortafuegos* | TR — *firewall* (loanword, standard) | EN — ファイアウォール (katakana transliteration, standard) | TR — 防火墙 (fánghuǒqiáng) | TR — جدار الحماية |
| Malware | EN (loanword widely used) | EN (loanword widely used) | TR — *malware* is itself the common term (treat as loanword) | TR — *malware* (loanword) | EN — マルウェア (katakana) | TR — 恶意软件 (èyì ruǎnjiàn) | TR — برمجيات خبيثة |
| Ransomware | EN (no natural FR equivalent in common use) | EN (loanword) | EN (loanword; *secuestro de datos* sounds like news-speak, not product copy) | EN (loanword) | EN — ランサムウェア (katakana) | TR — 勒索软件 (lèsuǒ ruǎnjiǎn) | TR — برمجيات الفدية |
| Scan (verb, product action) | TR — *analyser* | TR — *scannen* (loanword-verb, standard in software) | TR — *escanear* | TR — *escanear* | TR — スキャン (katakana, standard) | TR — 扫描 (sǎomiáo) | TR — فحص |
| Cloud (as in cloud protection) | EN in casual/marketing; TR *cloud/nuage* both seen — use *cloud* for consistency with product | EN — widely used as loanword in tech | TR — *nube* (well understood, natural) | TR — *nuvem* | EN — クラウド (katakana, dominant) | TR — 云 (yún) | TR — سحابة / أو الإبقاء على "كلاود" في السياقات التقنية |
| Subscription | TR — *abonnement* | TR — *Abonnement* | TR — *suscripción* | TR — *assinatura* | TR — サブスクリプション (katakana, standard for SaaS) | TR — 订阅 (dìngyuè) | TR — اشتراك |
| Dashboard | EN in fr-FR tech contexts (*tableau de bord* sounds automotive, not software) | TR — *Dashboard* (loanword, standard) | TR — *panel* or *tablero* (context-dependent, see locale note) | EN — *dashboard* (loanword, standard) | EN — ダッシュボード (katakana, standard) | TR — 仪表盘 (yíbiǎopán) or 控制面板 (kòngzhì miànbǎn) — use 控制面板 for product UI | TR — لوحة التحكم |
| Update (noun, software update) | TR — *mise à jour* | TR — *Update* (loanword, extremely common) or *Aktualisierung* (more formal, legal contexts) | TR — *actualización* | TR — *atualização* | TR — アップデート (katakana, standard) | TR — 更新 (gēngxīn) | TR — تحديث |
| Real-time protection | TR — *protection en temps réel* | TR — *Echtzeitschutz* | TR — *protección en tiempo real* | TR — *proteção em tempo real* | TR — リアルタイム保護 | TR — 实时保护 (shíshí bǎohù) | TR — الحماية في الوقت الفعلي |

**How to read this table:** "EN" doesn't mean "impossible to translate" — it means market research and existing convention show the English term is what practitioners and general users actually say. Using the "correct" native translation instead can make copy sound like it was written by someone unfamiliar with the category (a real risk in security software, where trust is the product).

---

## 4. Worked Example: Transcreating a Tagline

**Source (EN):** "Stay Warded."
*(Relies on wordplay: "warded" evokes both "guarded/protected" and the brand name "Warden," plus a slight play on "ward off.")*

| Locale | Approach | Result | Rationale |
|---|---|---|---|
| fr-FR | Transcreate, drop wordplay | *"Restez protégé."* ("Stay protected.") | No French wordplay preserves both the brand-name pun and natural phrasing; clarity wins over cleverness here. |
| de-DE | Transcreate, keep brand tie-in differently | *"Warden schützt. Sie entspannen."* ("Warden protects. You relax.") | German marketing tends to favor a two-beat structural rhythm over punning; this preserves brand-forward structure instead of the pun. |
| es-419 | Transcreate, drop wordplay | *"Protegido, siempre."* ("Protected, always.") | Literal *"Quédate Wardeado"* is not a real word and would confuse; go for rhythm instead. |
| pt-BR | Transcreate, drop wordplay | *"Sempre protegido."* | Same logic as es-419; avoid inventing a fake verb from the brand name. |
| ja-JP | Do not attempt wordplay; use direct benefit statement | *"守られている、その安心を。"* (roughly: "The peace of mind of being protected.") | Puns rarely transfer to Japanese marketing conventions, which favor emotional/benefit statements for security products. |
| zh-CN | Transcreate to 4-character-adjacent rhythm (common in CN ad copy) | *"随时守护。"* ("Guarding you at all times.") | Short, rhythmic phrasing matches CN ad conventions better than a literal rendering. |
| ar-SA | Transcreate, formal register | *"حماية دائمة."* ("Constant protection.") | MSA marketing skews toward dignified, formal phrasing; playful English wordplay doesn't map to expected tone. |

**Takeaway pattern:** taglines built on English wordplay almost never survive translation — the brief should always say "transcreate for equivalent feeling," not "translate this sentence."

---

## 5. Locale-Specific Notes

**fr-FR**
- Use *vous* throughout product and legal content. *Tu* is only acceptable in casual social media posts, and only with sign-off from the FR in-market reviewer.
- Avoid Anglicisms *except* where §3 specifies — French readers in security/tech contexts are comfortable with some English loanwords, but overuse outside those specified terms reads as lazy translation.

**de-DE**
- Default to *Sie* in UI and legal. Compound nouns are expected and normal — don't artificially break them up to "simplify."
- German UI copy runs long due to compounding; when translating buttons/labels, prioritize a shorter true synonym over truncating an accurate one awkwardly.

**es-419 (Latin America, neutral)**
- This is a *neutral* Latin American Spanish — avoid Mexico-specific, Argentina-specific, etc. vocabulary. When regional variants conflict (e.g., "computadora" vs. "ordenador"), use the pan-regional LatAm term (*computadora*), never the Spain term (*ordenador*), unless the asset is explicitly tagged es-ES.
- "Dashboard": *panel* is preferred for product UI (shorter, common in SaaS); *tablero* is acceptable in more general/marketing contexts.

**pt-BR**
- Do not use European Portuguese (pt-PT) vocabulary or verb conjugation patterns (e.g., use *você* forms, not *tu* conjugations common in pt-PT).
- Brazilian software UX conventions favor slightly more warmth than fr-FR or de-DE even in formal contexts — "você" register reads professional-friendly, not casual, so don't over-correct toward stiffness.

**ja-JP**
- Use *teineigo* (polite form, -desu/-masu) as the default register for UI and support content. Avoid *sonkeigo/kenjougo* (higher honorific tiers) in UI — it reads overly formal/stiff for software, almost bureaucratic.
- Katakana loanwords are the norm for most modern tech terms (see §3) — do not "translate down" into older Japanese equivalents; this reads as outdated, not more authentic.
- Sentence-final punctuation in UI is typically omitted or minimal compared to English; don't mechanically carry over English punctuation density.

**zh-CN**
- All content must use Simplified characters only — no mixing with Traditional forms.
- Any content referencing security incidents, government/state actors, or surveillance-adjacent topics requires an additional compliance review pass before translation is finalized, due to local regulatory sensitivity. Flag these assets explicitly when sent for translation.
- 控制面板 (control panel) is preferred over 仪表盘 (dashboard, literally "instrument panel") for in-product navigation; 仪表盘 is acceptable in marketing/analytics contexts.

**ar-SA**
- RTL layout: any content with embedded English terms (per §3 "EN" entries) requires bidi (bidirectional) formatting review — English substrings within RTL sentences need correct directional isolation to avoid visual scrambling. Flag to engineering/localization QA, not just the translator.
- Use Modern Standard Arabic (MSA / fusha), not Gulf, Levantine, or Egyptian dialect, regardless of the specific target country within the Arabic-speaking region.
- Numerals: use Western Arabic numerals (0–9) in UI and legal content for consistency with product design, not Eastern Arabic numerals (٠–٩), unless a specific in-market requirement says otherwise.

---

## 6. Do's and Don'ts Summary

| Do | Don't |
|---|---|
| Keep proper nouns (Warden, Warden Home) untranslated everywhere | Transliterate the brand name into local script unless instructed (e.g., no ワーデン unless a specific JP branding decision says otherwise) |
| Use the term table (§3) as the source of truth over personal preference | "Correct" a loanword into a native equivalent because it seems more proper |
| Flag legal terms with no clean equivalent | Approximate legal/contract terms to keep the sentence flowing |
| Transcreate taglines and headlines when briefed to do so | Transcreate UI microcopy or legal text |
| Match each locale's default formality register | Default to informal register to "sound friendlier" — formality ≠ coldness in most of these locales |
| Preserve exact numeric claims (percentages, stats) | Round, soften, or drop specific claims for smoother phrasing |

---

## 7. Query Log Process

Translators should log — not silently resolve — any of the following:
- A §3 term appearing in a context that doesn't match its documented usage
- Any legal clause with no clear jurisdictional equivalent
- Any instance where following this guide would produce copy that a native-speaking reviewer flags as unnatural

Queries are reviewed weekly by the in-market linguistic reviewer for each locale, and resolved answers are added back into this document to keep it current.
