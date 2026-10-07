<!-- المصادر: 6 محادثات DeepSeek مشاركة | نُفذ وحُفظ: 2026-10-08 بواسطة Qwen -->

# خريطة المحادثات الست → المستودعات (تنفيذ 2026-10-08)

ست محادثات DeepSeek إضافية عولجت بعد حزمة `fx7z2oxgpoiikvgihm`
(الموثقة في `2026-10-08-deepseek-handoff-package.md`). المنهجية نفسها:
استخراج كامل عبر API ← جرد المخرجات ← تدقيق وتصحيح ← دمج فيما يناسب ←
أرشفة ما لا يُدمج مع سبب صريح.

| المحادثة | الرسائل | الموضوع | المصير |
|---|---|---|---|
| `12p22z9mfd76f6i9f7` | 10 | مراجعة المستودعات + خطة دمج شاملة + ميزات مفتوحة المصدر | 📄 `docs/plans/2026-10-08-repos-strategy-review.md` — **أرشيف**: كودها استهدف بنية مثالية قديمة؛ الدمج كان سينشئ كودًا ميتًا (التوحيد الحقيقي تم عبر ocr-core/omni) |
| `2873vzbqibqh1ihe31` | 94 | الخط اليدوي العربي + jina + OpenCodeReview + Xberg + Stirling + VPS + docling + توحيد OCR | ✅ **omni-medical-suite** (PR #180): حزمة `omni_preprocess` (Stirling) + `tools/ahw-dataset-builder` + ‏14 عقد/برومبت في `docs/prompts/` + خطط البنية في `docs/future/` |
| `48pdrk6jj2uqy2li1c` | 38 | مصادر: نشرات دوائية عربية، قواميس ثنائية، TEDx، مدونات تدريب | ✅ **marathon-suite**: حملة `campaigns/medical-sources/` (7 ملفات بيانات + web_sources.yaml بحالة pending_wiring) |
| `xaxlwnipswawwn003s` | 2 | محلل 5 شخصيات → خطة إصلاح المحفظة | 📄 `docs/plans/2026-10-08-portfolio-repair-plan.md` — مرجع استراتيجي (البرومبت محفوظ كأداة قابلة لإعادة الاستخدام) |
| `ijn4bwu4rzbupprvhu` | 8 | نظام كتب الترجمة الطبية: تدقيق OCR + مواصفة معالجة 21 بندًا + OLMoCR | ✅ **medical-translation-intake** (مستودع جديد): خط معالجة fail-closed كامل منفَّذ + مختبَر (39 اختبارًا) |
| `pqmaahl9ccfybhvo85` | 2 | دفعة كتب (21 عنصرًا: قواميس Longman/Babylon، كتب ترجمة، مسارد، srt) | ✅ **medical-translation-intake**: `books/MANIFEST.yaml` (جرد + تصنيف + حالات + cross-refs لمستودعات قائمة) |

## المستودع الجديد: medical-translation-intake

أُنشئ تنفيذًا للطلب الصريح في `pqmaahl9ccfybhvo85` («أريد إضافة هذه الكتب
والملفات إلى github.com/DrAbdulmalek/medical-translation-intake» — لم يكن
موجودًا). يحتوي:

- `src/intake/` — 10 وحدات تنفذ مواصفة المعالجة (21 بندًا) من
  `ijn4bwu4rzbupprvhu`: بصمات 3 مستويات، manifest تذاكر idempotent،
  كشف تكرار بالمحتوى فقط، trusted-only KB + ترحيل بلا حذف، مصنّف
  تعريف≠ترجمة، تقييم أنماط موزون، مهايئ OCR **مربوط بـ ocr-core الفعلي**
  (تصحيح: المحادثة صممته فوق omni-ocr-core المقترح — الموجود هو ocr-core)
- 39 اختبارًا أخضر (المسار الذهبي REAL + ناشر MOCKED — مصنف وفق بند 15)
- `books/MANIFEST.yaml` — جرد الدفعة الأولى + cross-refs (dictionaries-csv،
  arabic-medical-glossary) لمنع الازدواج
- `docs/` — 5 وثائق مصدر مؤرشفة

## تصحيحات التدقيق المطبقة في هذه الدفعة

1. **omni_preprocess**: اختبارات المحادثة كانت تفشل حتمًا في CI (خادم حي +
   fixtures مفقودة) → skip-aware + اختبارات وحدة mock حقيقية (8 passed)
2. **ahw-dataset-builder**: أسماء ملفات وُضعت وفق الاستيرادات الفعلية
   (`templates/embed.py`، `train_dashboard.html`) — المحادثة سمت الأخيرة خطأً
3. **intake**: إصلاح شرط أسقط المصطلحات المفردة في استخراج الأزواج؛ تحقق
   مبكر من وجود الملف؛ نمط الجمل الوصلية الإنجليزية في المصنّف
4. **contracts omni-ocr-core**: كل العقود (C-00/C-01/Phase-1) فُهرست بحالة
   «تجاوزه ocr-core القائم» — منع بناء مستودع موازٍ مكرر
5. **web_sources.yaml**: المصادر بحالة `pending_wiring` صريحة — لا ادعاء
   أن حصادًا يعمل وهو لا يعمل

## ما لم يُنفذ (بأمانة)

- عقود التدقيق (AHW-01/XB-01/DOC-01/OCR-CR-01) **لم تُنفذ** — هي عقود
  لوكلاء منفذين ببوابات توقف، محفوظة في `omni-medical-suite/docs/prompts/`
- خطط VPS/Oracle/Codespaces/Colab — TEMPLATES ONLY (كما نصت المحادثة)
- ahw-dataset-builder لم يُشغَّل E2E (يحتاج PDF حقيقي + GPU للتدريب) —
  مصروف ومُتحقق استيراده فقط، وحالته موثقة في README
- ملفات الكتب الثنائية نفسها (PDF/MDX/ZIP) ليست في git — على جهاز المالك؛
  MANIFEST يوثقها وخطة معالجتها
