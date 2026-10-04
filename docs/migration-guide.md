# Migration Guide — نقل مشاريع الأسطولة إلى Harness موحّد

> دليل نقل المشاريع إلى بنية Harness موحّدة **بدون فقدان أي حالة قائمة**.
> مستند إلى منهجية Learn Harness Engineering (MIT) ومطبَّق فعلياً على
> أسطولة DrAbdulmalek في 2026-10-05.

> **ملاحظة تكييف**: في مساحة العمل هذه تسكن المستودعات في `repos/<اسم>`.
> تبنّي Harness تم عبر فرع `feat/harness-engineering` في كل مستودع + PR مسودة —
> **لا دفع إلى main ولا دمج PRs من طرف الوكيل؛ قرار الدمج للمالك وحده.**

## المشاريع المستهدفة (الأسطولة)

| المشروع | المستودع | البوابة | الحالة وقت التبنّي |
|---------|----------|---------|---------------------|
| ocr-core | `DrAbdulmalek/ocr-core` | `PYTHONPATH=src pytest tests/ -q` | main @ 7bdf3f4 — الواجهة العامة حقيقية (240 اختبار على الفرع المُصلَح) |
| translation-core | `DrAbdulmalek/translation-core` | `PYTHONPATH=src pytest tests/ -q` | main @ 841c2d7 |
| marathon_ted_pipeline | `DrAbdulmalek/marathon_ted_pipeline` | `pytest tests/ -q` + `ruff --select E9,F63,F7,F82` | main @ 3d043c5 |
| intelli-file-manager | `DrAbdulmalek/intelli-file-manager` | `pytest tests/unit -q` | main @ a6562a0 — بوابة ocr_gateway مركزية |
| marathon-suite | `DrAbdulmalek/marathon-suite` | `PYTHONPATH=src pytest tests/ -q` | v0.2.0 — حملة ortho حية |
| tg-campaign-toolkit | `DrAbdulmalek/tg-campaign-toolkit` | فحص صياغة بايثون لكل .py المتتبعة | PR مسودة #4 (سكربتات ortho) |
| channel-ops-dashboard | `DrAbdulmalek/channel-ops-dashboard` | `tsc --noEmit` (يتطلب node_modules) | PR مسودة #2 (edit-ocr v0.2) |
| manjaro-care | `DrAbdulmalek/manjaro-care` | `pytest tests/ -q` | فرع feature/tests-ci |
| omni-medical-suite | `DrAbdulmalek/omni-medical-suite` | `pytest --collect-only` (بوابة هيكلية) | بعد مراجعة Category B |

## استراتيجية عامة — 5 مراحل لكل مشروع

1. **الفحص** — ما موجود؟ ما مفقود؟ (`test -f AGENTS.md` ... إلخ)
2. **الحفظ** — نسخة احتياطية: `git bundle create ~/backups/<repo>-$(date +%Y%m%d).bundle --all`
3. **الإضافة** — تثبيت ملفات Harness **بلا مسّ الموجود** (`bootstrap.sh --force=0`).
4. **التخصيص** — تعديل `AGENTS.md` لكل مشروع (البوابة + النطاق + الأوامر).
5. **التحقق** — `./init.sh` + `./scripts/verify.sh` ثم commit على **فرع** وPR مسودة.

**قاعدة**: لا تُغيّر أي شيء جوهري في المشروع. فقط أضف طبقة Harness.

## ما يُثبَّت في كل مستودع

```
AGENTS.md                  ← العقد المخصص (v2.0)
feature_list.json          ← المهام وحالاتها
progress.md                ← السجل التراكمي
session-handoff.md         ← لقطة التسليم
init.sh                    ← بوابة الدخول (كشف تلقائي + بوابة المشروع)
scripts/verify.sh          ← بوابة ما قبل الالتزام + فحص أسرار
scripts/session-handoff.py ← مولّد التسليم + حفظ Mem0 اختياري
scripts/test_mem0_memory.py← اختبار الذاكرة عبر الجلسات
docs/HARNESS.md            ← الدليل المفهومي
```

وفي `marathon-suite` (المركز) إضافةً: `templates/` + `docs/migration-guide.md`.

## أخطاء شائعة تجنّبها

| الخطأ | الصواب |
|-------|--------|
| تشغيل bootstrap بـ --force على مشروع قائم | بلا --force: يضيف المفقود فقط |
| دمج .gitignore بلا مراجعة | قارن القواعد قبل الدمج |
| نسيان تخصيص AGENTS.md | كل مشروع مختلف — البوابة والنطاق |
| تشغيل session-handoff.py بلا --note | الملاحظة هي قيمة التسليم |
| حفظ أسرار في Mem0 | لا — القاعدة صفرية 6 |
| تشغيل verify.sh **بعد** commit | شغّله **قبل** الالتزام |
| العمل مباشرة على main | فرع feat/* ثم PR مسودة |

## ما بعد الترحيل

1. **اربط pre-push hook** (اختياري): `.git/hooks/pre-push` يستدعي `./scripts/verify.sh --quick` ويمنع الدفع عند الفشل.
2. **فعّل Mem0**: `export MEM0_API_KEY=...` ثم `python3 scripts/test_mem0_memory.py` للتحقق عبر الجلسات.
3. **وسّع**: أضف مشاريع جديدة بنفس البروتوكول عبر `templates/scripts/bootstrap.sh`.
4. **فرق الوكلاء**: عند الحاجة، استخدم LobeHub لتشغيل فرق وكلاء فوق نفس الـ Harness (كل وكيل يقرأ AGENTS.md نفسه).

## قائمة تحقق التبنّي

- [x] كل مستودع له فرع `feat/harness-engineering` يحمل الملفات العشرة
- [x] `bash -n init.sh` و`python3 -m py_compile` ناجحان في كل مستودع
- [ ] مراجعة المالك ودمج PRs المسودة (قرار المالك وحده)
- [ ] Mem0 MCP مفعّل في أداة واحدة على الأقل + أول اختبار عبر الجلسات
- [ ] pre-push hook موصول في المستودعات النشطة
