# حزمة جاهزية إصدار ocr-core v0.7.0 (S1-T3)

> **تاريخ التدقيق:** 2026-10-08 | **الحالة النهائية:** `READY_FOR_TAG` — **إنشاء الوسم إجراء المالك وحده** (READY_FOR_TAG ≠ TAG AUTHORIZED).

## 1) الأساس مقابل الحالة الحية (استعلام 2026-10-08)

| البند | الأساس (العقد) | الحالة الحية | التغيير |
|---|---|---|---|
| pyproject.toml version | 0.7.0 | 0.7.0 | بلا تغيير |
| آخر وسم | v0.6.0 | v0.6.0 (يؤشر على 79b07be — تحقق `git rev-parse v0.6.0^{commit}`) | بلا تغيير |
| وسم v0.7.0 | غائب | **ما زال غائباً** | بلا تغيير |
| main SHA | — | `e61683f7590d9f22c163af103a75f3c3e6db42b3` | مسجل كأساس المهمة |

## 2) مراجعة v0.6.0…main

- **3 commits فقط:** c0b76af (دمج PR#52 — pipeline ست المراحل، أصدر ضمن v0.6.0) و9b08821/e61683f (PR#53 — نظام أوامر موحد 34 أمراً + كشف كلمات + jina-ocr-v1، موسوم نصياً [v0.7.0]).
- **36 ملفاً: +4,066 / −3.** الأسطر المحذوفة الثلاثة (دليل مباشر من `git diff v0.6.0..main`): `version = "0.6.0"`، سطر الوصف، وقائمة `all` extras — **كلها استبدال/توسيع، لا كسر واجهة**.
- **جديد في 0.7.0:** `ocr_core.commands` (CLI موحد `ocr-core` عبر `[project.scripts]`)، `preprocess/word_detector` + `line_grouper`، محرك `engines/jina_vlm`، extras جديدة: `word-detect`، `jina`، `vlm`، `pdf`، `docx`. ملاحظة ترخيص موثقة داخل pyproject: أوزان jina **CC BY-NC 4.0** (الكود MIT) و`all` يستثنيها عمداً.
- **تقييم الكسر:** صفر استثناءات API محذوفة؛ كل التغييرات إضافية. **لا كسر توافق.**

## 3) الاختبارات (إعادة تشغيل محلية على نفس أساس main)

```
Command: pip install -e ".[preprocess,benchmarks,golden]" && pytest -q
Result:  490 passed, 7 skipped in 15.53s   (main e61683f, شجرة نظيفة — git status = 0)
```
(ملاحظة منهجية: تشغيل الاختبارات بمجرد `PYTHONPATH=src` يفشل في الاستيراد لأن `ocr_core/charter_v2.yaml` يُقدم عبر الحزمة من جذر المستودع — التثبيت القابل للتعديل هو المسار الصحيح، وهو نفسه ما يفعله CI.)

## 4) CI الحي على main

| Workflow | الفرع | SHA | النتيجة | التوقيت (UTC) |
|---|---|---|---|---|
| tests | main | e61683f | **success** | 2026-10-07T21:34:24Z |

## 5) اتساق الإصدار + فجوة التغيير الموثق

- pyproject=0.7.0 ✓ | commit PR#53 يحمل [v0.7.0] ✓ | **فجوة واحدة:** `CHANGELOG.md` **لا يحتوي قسماً بعنوان 0.7.0** — أقسامه العليا ما زالت «غير مُصدر» لفروع أخرى (abbyy-cleanroom وauto-ink-contrast وgolden-sample-cer، لم تُدمج). ملفات PR#53 موثقة في CHANGELOG ضمنياً عبر نص الـPR لا عبر قسم إصدار.
- **مسودة ملاحظات الإصدار (جاهزة للاعتماد):** v0.7.0 = نظام أوامر موحد (34 أمراً: ocr/preprocess/postprocess/detect/export/benchmark/vlm) + كشف كلمات الخط اليدوي (ONNX، extra `word-detect`) + محرك `jina-ocr-v1` (extra `jina`/`vlm`؛ أوزان CC BY-NC لأغراض غير تجارية) + PDF/DOCX I/O. إضافي فقط، لا كسر.

## 6) شجرة العمل ونطاق الوسم

- شجرة main نظيفة (git status = 0 تغيير) ✓
- الوسم المقترح: `v0.7.0` مؤشراً على **e61683f** (رسالة مقترحة: "v0.7.0: unified command system (34 cmds) + handwriting word detection + jina-ocr-v1 engine").

## 7) بوابة القرار

| البند | الحالة |
|---|---|
| تدقيق جاهزية مكتمل | ✓ (§1–§6) |
| ملاحظات إصدار | جاهزة (مسودة §5) — اعتماد CHANGELOG الرسمي يُنفذ مع الوسم |
| اختبارات | 490 passed / 7 skipped محلياً |
| CI على main | GREEN |
| كسر غير مفسّر | **لا يوجد** |
| تفويض المالك قبل الوسم | **مطلوب — غير ممنوح بعد** |

**الحالة: READY_FOR_TAG.** إن وافق المالك: `git tag -a v0.7.0 e61683f -m "..." && git push origin v0.7.0`.
