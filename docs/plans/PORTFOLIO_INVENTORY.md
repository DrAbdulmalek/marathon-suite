<!-- PORTFOLIO_INVENTORY.md — Phase 0.1+0.2 من خطة الإصلاح العملية (docs/plans/2026-10-08-portfolio-repair-plan.md) -->
<!-- مولَّد آليًا من GitHub API بتاريخ 2026-10-08 — لقطة زمنية قابلة لإعادة التوليد -->

# الجرد الجنائي الموحد لمحفظة المستودعات (PORTFOLIO_INVENTORY)

المرجع الحاكم: [خطة الإصلاح العملية لمحفظة المستودعات](2026-10-08-portfolio-repair-plan.md) — المرحلة 0.
القاعدة: ملف جرد واحد بدل عشرين تقريرًا؛ يُعاد توليده آليًا عند الحاجة.

## ملخص الأرقام

- إجمالي المستودعات المملوكة: **52**
- إجمالي الـ PRs المفتوحة: **123** (هدف المرحلة 0: الوصول إلى 0 عبر دمج أو إغلاق واعٍ)
- الأنشطة (دفع خلال 7 أيام): **30**
- التوزيع المقترح للتصنيف: Asset=6، Core=14، Dead=13، Duplicate=7، Tooling=12

## ملاحظات القراءة

- عمود **التصنيف** هو *مقترح* آلي وفق معايير المرحلة 0.2 (Core/Asset/Tooling/Duplicate/Dead).
- **قرار الأرشفة/الحذف قرار مالك وحده** — لا يُنفذ آليًا مهما كانت التوصية.
- "مكرر" يعني: يكرر وظيفة مستودع آخر حيّ؛ الملاحظة تحدد الضدّ.

## الجدول الكامل (52 مستودعًا، مرتبة بآخر دفع)

| # | المستودع | خاص | آخر دفع | فروع | PRs مفتوحة | الترخيص | التصنيف (مقترح) | الإجراء المقترح |
|---|---|---|---|---|---|---|---|---|
| 1 | omni-medical-suite | 🌍 | 2026-10-08 | 100 | 43 | MIT | Core | إبقاء — تطوير نشط |
| 2 | dictionaries-csv | 🌍 | 2026-10-08 | 5 | 0 | NOASSERTION | Core | إبقاء — تطوير نشط |
| 3 | marathon-suite | 🌍 | 2026-10-08 | 12 | 1 | MIT | Core | إبقاء — تطوير نشط |
| 4 | arabic-medical-handwriting | 🌍 | 2026-10-08 | 1 | 0 | MIT | Core | إبقاء — تطوير نشط |
| 5 | medical-rag-ar | 🌍 | 2026-10-08 | 1 | 0 | MIT | Core | إبقاء — تطوير نشط |
| 6 | ortho-books-sync | 🔒 | 2026-10-08 | 1 | 0 | MIT | Core | إبقاء — تطوير نشط |
| 7 | medical-translation-intake | 🔒 | 2026-10-07 | 3 | 0 | MIT | Core | إبقاء — تطوير نشط |
| 8 | intelli-file-manager | 🌍 | 2026-10-07 | 51 | 11 | MIT | Core | إبقاء — تطوير نشط |
| 9 | ocr-core | 🌍 | 2026-10-07 | 36 | 3 | MIT | Core | إبقاء — تطوير نشط |
| 10 | tg-campaign-toolkit | 🔒 | 2026-10-07 | 8 | 5 | — | Core | إبقاء — تطوير نشط |
| 11 | marathon_ted_pipeline | 🌍 | 2026-10-07 | 24 | 14 | — | Core | إبقاء — تطوير نشط |
| 12 | gdrive-telegram-tools | 🔒 | 2026-10-07 | 1 | 0 | — | Tooling | إبقاء بلا تطوير |
| 13 | channel-ops-dashboard | 🔒 | 2026-10-07 | 11 | 2 | — | Tooling | إبقاء بلا تطوير |
| 14 | DrAbdulmalek | 🌍 | 2026-10-07 | 2 | 0 | — | Tooling | إبقاء بلا تطوير |
| 15 | telegram-tools | 🌍 | 2026-10-07 | 15 | 9 | MIT | Tooling | إبقاء بلا تطوير |
| 16 | repo-sync-toolkit | 🌍 | 2026-10-07 | 6 | 0 | MIT | Tooling | إبقاء بلا تطوير |
| 17 | arabic-medical-glossary | 🌍 | 2026-10-06 | 3 | 0 | MIT | Asset | إبقاء — حماية بيانات |
| 18 | glossary-api | 🌍 | 2026-10-06 | 1 | 0 | MIT | Tooling | إبقاء بلا تطوير |
| 19 | handwriting-notes | 🔒 | 2026-10-06 | 1 | 0 | — | Core | إبقاء — تطوير نشط |
| 20 | zai-sessions | 🔒 | 2026-10-06 | 1 | 0 | — | Tooling | إبقاء بلا تطوير |
| 21 | manjaro-care | 🌍 | 2026-10-05 | 20 | 2 | MIT | Tooling | إبقاء بلا تطوير |
| 22 | zai-workspace | 🔒 | 2026-10-05 | 1 | 0 | — | Dead | مقرح: أرشفة فورية (قرار المالك) |
| 23 | omni-medical-dictionaries | 🌍 | 2026-08-02 | 3 | 1 | MIT | Asset | إبقاء — حماية بيانات |
| 24 | omni-ocr-training-db | 🔒 | 2026-10-05 | 1 | 0 | — | Asset | إبقاء — حماية بيانات |
| 25 | finereader-ocr-apk-analysis | 🌍 | 2026-10-04 | 2 | 1 | — | Tooling | إبقاء بلا تطوير |
| 26 | translation-core | 🌍 | 2026-10-04 | 3 | 1 | MIT | Duplicate | مقترح: أرشفة (قرار المالك) — دوره اندمج في medical-translation-bot |
| 27 | medical-translation-bot | 🔒 | 2026-10-04 | 4 | 1 | MIT | Core | إبقاء — تطوير نشط |
| 28 | translation-knowledge-base | 🔒 | 2026-10-04 | 3 | 0 | MIT | Core | إبقاء — تطوير نشط |
| 29 | omni-medical-suite_dict | 🔒 | 2026-10-04 | 2 | 0 | NOASSERTION | Duplicate | مقترح: أرشفة (قرار المالك) — غالبًا سبقه omni-medical-dictionaries |
| 30 | medical-ocr-trainer-hf | 🌍 | 2026-10-04 | 2 | 0 | MIT | Dead | مقرح: أرشفة فورية (قرار المالك) — أحدث من medical-ocr-trainer — أبقِ أحدهما |
| 31 | medical-translation-knowledge | 🔒 | 2026-09-06 | 2 | 0 | — | Duplicate | مؤرشف بالفعل — غالبًا سبقه translation-knowledge-base |
| 32 | translation-book-intake | 🔒 | 2026-09-05 | 2 | 0 | — | Duplicate | مؤرشف بالفعل — سبقه medical-translation-intake |
| 33 | medical-ocr-archived | 🔒 | 2026-08-01 | 2 | 0 | — | Dead | مؤرشف بالفعل |
| 34 | sync-github | 🌍 | 2026-08-02 | 3 | 1 | MIT | Duplicate | مؤرشف بالفعل — الخطة نصّت: أرشفته نهائيًا لصالح repo-sync-toolkit |
| 35 | omni-medical-workspace | 🔒 | 2026-10-03 | 3 | 0 | — | Duplicate | مؤرشف بالفعل — تداخل مع zai-workspace/workspace-scripts-archive |
| 36 | workspace-scripts-archive | 🌍 | 2026-09-25 | 1 | 0 | — | Tooling | مؤرشف بالفعل |
| 37 | translearners-archive | 🔒 | 2026-09-24 | 1 | 0 | — | Dead | مؤرشف بالفعل |
| 38 | omni-handwriting-samples-private | 🔒 | 2026-09-23 | 1 | 0 | — | Asset | إبقاء — حماية بيانات |
| 39 | malek_data | 🔒 | 2026-09-05 | 3 | 1 | — | Asset | مؤرشف بالفعل |
| 40 | reset-net | 🌍 | 2026-08-01 | 2 | 1 | MIT | Dead | مقرح: أرشفة فورية (قرار المالك) |
| 41 | manjaro-doctor | 🌍 | 2026-08-13 | 1 | 0 | MIT | Tooling | إبقاء بلا تطوير |
| 42 | medical-ocr-demo | 🌍 | 2026-08-02 | 1 | 0 | MIT | Dead | مقرح: أرشفة فورية (قرار المالك) |
| 43 | OmniFile_Processor | 🌍 | 2026-08-01 | 2 | 0 | NOASSERTION | Dead | مقرح: أرشفة فورية (قرار المالك) |
| 44 | glossary-collector | 🔒 | 2026-08-01 | 1 | 0 | — | Tooling | إبقاء بلا تطوير |
| 45 | radiology-ai-platform | 🌍 | 2026-08-01 | 1 | 0 | Apache-2.0 | Dead | مقرح: أرشفة فورية (قرار المالك) |
| 46 | medical-ocr-benchmarks | 🌍 | 2026-07-07 | 1 | 0 | MIT | Dead | مؤرشف بالفعل |
| 47 | medical-ocr-trainer | 🌍 | 2026-07-07 | 5 | 4 | MIT | Duplicate | مؤرشف بالفعل — غالبًا سبقه medical-ocr-trainer-hf |
| 48 | medical-ocr-ground-truth | 🌍 | 2026-07-07 | 10 | 9 | — | Asset | مؤرشف بالفعل |
| 49 | scanner-fixer | 🌍 | 2026-07-07 | 6 | 5 | MIT | Dead | مؤرشف بالفعل |
| 50 | medical-ocr-training-hub | 🌍 | 2026-07-07 | 4 | 3 | MIT | Dead | مؤرشف بالفعل |
| 51 | arabic-medical-ocr-baseline | 🌍 | 2026-07-07 | 1 | 0 | — | Dead | مؤرشف بالفعل |
| 52 | medical-handwriting-ocr | 🌍 | 2026-07-07 | 6 | 5 | MIT | Dead | مؤرشف بالفعل |

## المرحلة 0.3 — نزيف الوكلاء (حالة التنفيذ)

- [x] نقل 7 ملفات مخرجات وكلاء من جذر omni-medical-suite إلى `docs/archive/agent-artifacts/` (PR منفصل بنفس هذا التاريخ).
- [ ] إغلاق/دمج الـ PRs المفتوحة الـ 123 (قائمة في الجدول أعلاه) — قرار مالك لكل PR.
- [ ] قاعدة حاكمة: لا وكيل يكتب documentation خارج docs/ (مطبقة في هذا المستودع منذ خطة الإصلاح).
