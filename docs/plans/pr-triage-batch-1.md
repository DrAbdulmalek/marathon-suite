# تصنيف دفعة PRs — الدفعة 1 (S1-T4)

> **تاريخ الاستعلام الحي:** 2026-10-08. **الأساس:** 123 PR مفتوحاً (2026-10-08)، 43 منها في omni-medical-suite.
> **هذه الدفعة:** أقدم 30 PR مفتوحاً في omni-medical-suite (الأقدم ← الأحدث)، بترتيب API `created asc`.
> **قاعدة العقد:** التصنيف فقط — **لا تنفيذ** لأي توصية هنا (لا دمج/إغلاق).
> **الأدلة لكل صف:** حالة check-runs لرأس الـ PR وقت الاستعلام (GitHub API حي).

## 1) ملاحظة بنيوية مهمة (الدليل أولاً)

**28 من 30 رأس PR أحمر CI**، بما في ذلك كل PRs dependabot منذ 2026-07-18. الأحمر إذن **ضوضاء خط أساس مستمرة** في omni-medical-suite، لا انعكاساً لجودة الـ PRs الفردية. التوصية البنيوية: مهمة «إصلاح CI خط الأساس» في omni-medical-suite تسبق أي إعادة تقييم جماعية — وإلا فكل تصنيف هنا سيظل NEEDS_REWORK لسبب واحد خارج نطاق كل PR.

## 2) الدفعة 1 — أقدم 30

| PR | العنوان | أُنشئ | الفرع | CI على الرأس | التوصية | ملاحظة/دليل |
|---|---|---|---|---|---|---|
| #53 | dependabot: actions/upload-artifact 4→7 | 2026-07-18 | dependabot/github_actions/actions/upload | red | DEFER | ضوضاء خط الأساس؛ تجميع ترقيات Actions في PR واحد بعد إصلاح CI |
| #55 | dependabot: docker/metadata-action 5→6 | 2026-07-18 | dependabot/.../docker/metadat | red | DEFER | كالسابق |
| #70 | docs(v1.2.0): README badges + release notes | 2026-07-31 | docs/v1.2.0-readiness | red | NEEDS_REWORK | عمره 69 يوماً؛ إعادة أساس + CI |
| #78 | dependabot: prometheus-fastapi-instrumentator | 2026-08-01 | dependabot/pip/prometheus-... | red | DEFER | تُدمج مع دفعة pip |
| #81 | dependabot: img2pdf ≥0.6.3 | 2026-08-01 | dependabot/pip/img2pdf-gte-0.6.3 | red | DEFER | كالسابق |
| #82 | dependabot: numpy <3 | 2026-08-01 | dependabot/pip/numpy-gte-1.24.0-and-lt-3 | red | DEFER | كالسابق |
| #83 | dependabot: pdfplumber ≥0.11.10 | 2026-08-01 | dependabot/pip/pdfplumber-gte-0.11.10 | red | DEFER | كالسابق |
| #84 | dependabot: pydantic <3? | 2026-08-01 | dependabot/pip/pydantic-gte-2.0.0-and-lt | red | DEFER | كالسابق |
| #86 | fix(security): إغلاق ثغرات ما بعد #85 | 2026-08-25 | hardening/post-85-audit-fixes | red | NEEDS_REWORK | أمني ذو قيمة — يستحق إحياء بعد إصلاح CI |
| #90 | Security fixes: medical OCR separator + admin auth | 2026-08-25 | security-fixes-clean | red | NEEDS_REWORK | كالسابق |
| #102 | fix(security): harden snapshot exporter | 2026-08-29 | fix/snapshot-security-hardening | red | NEEDS_REWORK | كالسابق |
| #107 | dependabot: click ≥8.5.0 | 2026-09-01 | dependabot/pip/click-gte-8.5.0 | red | DEFER | دفعة pip |
| #115 | fix(audit): harden production deployment | 2026-09-03 | fix/post-114-production-audit | red | NEEDS_REWORK | أمني |
| #116 | fix(ci): entrypoint validation hardening | 2026-09-03 | fix/ci-release-hardening-followup | red | NEEDS_REWORK | أمني/CI |
| #117 | feat(calibre-ocr): medical library | 2026-09-04 | feat/calibre-ocr-medical-library | red | DEFER | **مسودة** — قرار اتجاه مطلوب من المالك |
| #120 | feat(api): openFDA وغيرها | 2026-09-09 | feat/p0-public-api-integrations | red | NEEDS_REWORK | نطاق كبير |
| #121 | feat(enrichment): ICD-11 عربي | 2026-09-09 | feat/medical-terminology-enrichment | red | NEEDS_REWORK | نطاق كبير |
| #124 | PHASE 1+2: central OCR foundation + GT588 | 2026-09-18 | feat/seg-eval-gt588 | red | NEEDS_REWORK | متداخل مع توحيد ocr-core — إعادة أساس |
| #125 | PHASE 3/TASK 012: word seg fix | 2026-09-18 | feat/task012-word-seg-fix | red | NEEDS_REWORK | تابع #124 |
| #130 | security: quarantine Telegram Forwarder (Wave 1.4) | 2026-09-21 | security/quarantine-telegram-forwarder | red | NEEDS_REWORK | من موجة أمنية سابقة |
| #131 | security: SEC-2 env token-shape guard (Wave 1.2) | 2026-09-21 | security/sec2-env-token-shapes | red | NEEDS_REWORK | يتقاطع مع S1-T5 — تنسيق مطلوب |
| #132 | security: HF upload OFF + de-identification | 2026-09-21 | security/hf-privacy-gate | red | NEEDS_REWORK | خصوصية — أولوية داخل الأحمر |
| #133 | chore: root hygiene — 22 تقريراً إلى docs/ | 2026-09-21 | chore/root-hygiene | red | NEEDS_REWORK | تنظيفي |
| #134 | docs: OLMoCR + Xberg verification | 2026-09-21 | docs/olmocr-xberg-verification | red | NEEDS_REWORK | توثيقي |
| #135 | feat: Xberg package + OLMoCR adapter | 2026-09-23 | feat/xberg-olmocr-integration | red | NEEDS_REWORK | تابع #134 |
| #136 | feat(atr): TrOCR advanced pipeline | 2026-09-23 | feature/atr-trocr-advanced | red | NEEDS_REWORK | نطاق كبير |
| #143 | docs(audit): MISTRAL_REPOSITORY_AUDIT | 2026-09-28 | docs/mistral-repo-audit | red | NEEDS_REWORK | توثيقي |
| #144 | fix(evaluation): symmetric normalize_v1 (F-13) | 2026-09-29 | gs/f13-symmetric-normalization | red | NEEDS_REWORK | تقييم — قريب من الجاهزية |
| #145 | feat(evaluation): --set-dir | 2026-09-29 | gs/f14-set-dir | **green** | **SAFE_TO_MERGE** | الوحيدان الأخضران في الدفعة — قرار الدمج للمالك |
| #146 | fix(evaluation): LFS pointers fail loudly | 2026-09-29 | gs/lfs-golden-set-text | **green** | **SAFE_TO_MERGE** | كالسابق |

## 3) الملخص العددي

| التوصية | العدد |
|---|---|
| SAFE_TO_MERGE | 2 (#145، #146) |
| NEEDS_REWORK | 20 |
| DEFER | 8 (#53 #55 #78 #81 #82 #83 #84 #107 #117 — ضمنها مسودة #117) |
| CLOSE | 0 (لا يوجد دليل كافٍ على إغلاق أي منها — لا تخمين) |

## 4) التقدم التراكمي

- دفعة 1: 30 من 43 في omni-medical-suite (المدفوع من أساس 123 الكلي).
- الدفعتان 2-3 (S3-T4) والنهائي (S4-T2) تُبدآن باستعلام GitHub حي جديد دائماً.
