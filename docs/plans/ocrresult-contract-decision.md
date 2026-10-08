# قرار عقد OCRResult الموحّد — الحسم بمعيار المستهلكين الحقيقيين (S2-T3، تحديث §1.1)

> التاريخ: 2026-10-08 | المصدر: خطة الجاهزية للإنتاج §1.1 (توجيه المالك).
> هذه وثيقة **قرار** لا تدقيق — تُلغي «الشكل القانوني المقترح» في `ocrresult-contract-audit.md`
> (التصميم المدمج 12-حقلًا) وفق القاعدة الحاكمة الجديدة.

## القاعدة الحاكمة (توجيه المالك)

> **الذي له مستهلكون حقيقيون أكثر الآن يفوز — لا الأحدث زمنيًا. لا يُصمَّم عقد ثالث.**
> بعد القرار: المستودع الخاسر يحصل على shim إعادة تصدير، لا حذف.

## تصحيح مقدمات أولًا (تحقق حي 2026-10-08)

1. **omni PR #184 لا يحتوي أي OCRResult** — فحص diff الحي (6 ملفات: `benchmark_metrics.py` ‎+109،
   `build_benchmark.py`، `run_e2e.sh`، `test_benchmark_metrics.py`، `ui_app.py`، README): محتواه
   طبقة قياس (`cer`/`wer`/`normalize_arabic`/`Manifest`) بلا فئة OCRResult. «عقد omni» الفعلي
   يعيش في `packages/omni_ocr/adapter.py` وما شابه.
2. **التجزئة أعمق من «8 فروقات»**: يوجد **أربعة أشكال حية** للعقد في المحفظة، لا شكلان.

## الجرد الحي للأشكال الأربعة (AST على المصادر الحية، 2026-10-08)

| الشكل | الموقع | الحقول | فروق جوهرية عن النواة |
|---|---|---|---|
| **ocr-core** (المرشّح) | `src/ocr_core/engines/base.py:15` | **7**: text, engine, confidence, processing_time, error, pages, meta | — (المرجع) |
| omni-adapter | `packages/omni_ocr/adapter.py` | **13**: + word_count, words, raw_result, confidence_is_estimate, pdf_sha256, model, cloud, cost_estimate_usd | error من نوع `str=''` لا `Optional[str]` |
| omni-pipeline | `apps/ocr-pipeline/src/engines/base_engine.py` | **7**: text, confidence, bbox, **engine_name**, processing_time, word_level, **metadata** | تسمية مختلفة للحقلين الحاكمين |
| AMH | `ocr/contract.py` | **11**: + words[WordBox], language, duration_ms, raw_text, metadata, warnings, created_at | duration_ms بالمللي ثانية صراحة |

## المستهلكون الحقيقيون الآن (أسطر استيراد فعلية، grep على الاستنساخات الحية)

| العقد | أسطر الاستيراد | أين | الحكم |
|---|---|---|---|
| **ocr-core** | **13 داخليًا + 21 مرجعًا في جسر tg-campaign-toolkit** (`app_ocr/ocr_core_bridge.py` — «المستهلك الثاني لـ ocr-core» توثيقه الحي) | ocr-core + tg | **الفائز بفارق ساحق** |
| omni-adapter | 1 (إعادة تصدير `packages/omni_ocr/__init__`)؛ pipeline يستخدم شكله الخاص | omni | مجزأ داخليًا |
| AMH | 3 (ocr/__init__, ocr/engine.py, tests/test_contract.py) | AMH | محلي فقط |
| marathon_ted_pipeline / marathon-suite | 0 / 0 | — | مtp يعمل بـdicts لا بفئة |

## القرار

**العقد القانوني الموحد = OCRResult في ocr-core (7 حقول) حرفيًا، بلا أي تصميم ثالث.**

### جدول القرار لكل حقل (اتحاد حقول الأشكال الأربعة)

| الحقل | ocr-core | omni-adapter | AMH | القرار |
|---|---|---|---|---|
| text | ✓ | ✓ | ✓ | قانوني مشترك |
| engine | ✓ `str=''` | ✓ | ✓ `'unknown'` | قانوني؛ `engine_name` (pipeline) = alias تقادم في shim |
| confidence | ✓ `0.0=مجهول` (R15) | ✓ | ✓ | قانوني + تعميم سياسة «يُمنع اختلاق رقم» على الجميع |
| processing_time | ✓ | ✓ | `duration_ms` (ms) | قانوني؛ **الوحدة توثَّق الآن: ثوانٍ**؛ AMH يحوّل ÷1000 في shim |
| error | ✓ `Optional[str]` | `str=''` | `Optional[str]` | قانوني؛ shim الـadapter يوحّد `''→None` |
| pages | ✓ `1` | ✗ | ✗ | قانوني (مطلوب لـPDF) |
| meta | ✓ dict | `metadata`؟ لا — بلا | `metadata` | **الاسم القانوني `meta`**؛ أي فائض يذهب إليه |
| words/raw_result/confidence_is_estimate/pdf_sha256/model/cloud/cost_estimate_usd | ✗ | ✓ | words ✓ | **→ `meta`** عبر shims (لا حقول جديدة) |
| language/raw_text/warnings/created_at/bbox/word_level | ✗ | ✗/bbox ✓ | ✓ | **→ `meta`** عبر shims |

### حالة shims المستودعات الخاسرة

| المستودع | الحالة | الدليل |
|---|---|---|
| **arabic-medical-handwriting** | **منفَّذ — PR ‏AMH#1** (`sprint2/s2t3-canonical-shim`): `ocr/canonical.py` بـ`CANONICAL_FIELDS` مجمدة + `to_canonical()` (كل حقل يهبط في مكان موثق، ms→s، تدهور آمن بلا ocr-core) + `tests/test_contract_parity.py` (17 passed محليًا) | PR AMH#1 |
| omni-adapter + omni-pipeline | **مُحدَّد — الخطوة التالية من S2-T3** (بعد دمج #184 لتجنب تضارب الفرع): shim يعيد التصدير من الشكل القانوني + حقن الفائض في `meta`؛ يُقيد بـOD-008 | OD-008 |
| omni-pipeline (engine_name/metadata) | نفس الدفعة: alias تقادم + إعادة تسمية تدريجية | OD-008 |

### PRs المقترنة المنفذة في هذه الموجة (v4.0 §22)

| PR | المحتوى |
|---|---|
| ocr-core **#56** | `ocr_core.eval`: `calculate_cer/wer(..., skip_internal_normalize=False)` + `normalize_v1` مُعلنة الإصدار + `scripts/golden_harness.py` (تطبيع الطرفين مرة واحدة) — 504 passed/7 skipped، ruff نظيف |
| omni **#185** | توافق harness: المرجع يُطبَّع عبر normalize_v1 أيضًا + `skip_internal_normalize=True` + provenance للطرفين — إغلاق F-13/F-16 |
| omni **#186** | تصحيح A1: المرجع الحاكم لـarabic_rtl.py = `packages/nlp/arabic_rtl.py` |
| AMH **#1** | shim العقد القانوني (فوق) |

### لماذا رُفض «الشكل المدمج المقترح» في تدقيق S2-T3؟

كان يضيف 5 حقول جديدة إلى النواة (`duration_ms`, `words`, `language`, `raw_text`, `warnings`, `created_at`)
= **تصميم ثالث** يخالف القاعدة الحاكمة. فوائده محفوظة كاملة: الوحدة الصريحة أصبحت توثيقًا
(`processing_time` = ثوانٍ)، وحقول AMH الفائضة تنتقل إلى `meta` عبر الجسر، واختبار التكافؤ
المجمد يمنع الانزلاق — دون لمس توقيع النواة ولا كسر مستهلكيها الـ34.
