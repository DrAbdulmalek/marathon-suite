# docs/handoff — حزم التسليم والقرارات عبر المستودعات

هذا المجلد يؤرشف حزم التسليم القابلة للتنفيذ (prompts + قوائم رفع +
تسلسلات اختبار) المتبادلة بين أدوات الذكاء (DeepSeek/Z.ai/Qwen/genspark)
ومستودعات مجموعة الماراثون، مع نتيجة التنفيذ الفعلي لكل حزمة.

## الفهرس

| الوثيقة | المصدر | الحالة |
|---|---|---|
| `2026-10-08-deepseek-handoff-package.md` | محادثة DeepSeek [fx7z2oxgpoiikvgihm](https://chat.deepseek.com/share/fx7z2oxgpoiikvgihm) — الرسالة 151 | ✅ نُفِّذت (ocr-core v0.7.0 + intelli-file-manager) |

## خريطة محادثة DeepSeek → المستودعات (تنفيذ 2026-10-08)

المحادثة (152 رسالة، ~680 كتلة كود) غطت مسار "الماراثون" كاملًا.
ما استُخرج ودُقِّق ورُفع فعليًا:

| محتوى المحادثة | الرسائل | المستودع الهدف | الحالة |
|---|---|---|---|
| ميثاق قواعد OCR ‏(18 قاعدة — Visual Evidence Charter) | 0-1 | `ocr-core` (rules/) + `marathon_ted_pipeline` (config/marathon_ocr_rules.yaml) | موجود مسبقًا — تحقق تطابق ✅ |
| خط أنابيب TED (ted_fetcher/pdf_ocr/epub_ocr/translator/telegram_uploader/marathon_runner) | 3-9 | `marathon_ted_pipeline` | موجود مسبقًا (src/*) ✅ |
| المصادقة + الطوابير + النشر (auth/queue_worker/deploy) | 11 | `marathon_ted_pipeline` | موجود مسبقًا ✅ |
| المراقبة (metrics/prometheus/grafana/alertmanager) + بوت تيليجرام + webhooks | 13 | `marathon_ted_pipeline` | موجود مسبقًا ✅ |
| K8s + ted2srt_py | 15-19 | `marathon_ted_pipeline` | موجود مسبقًا ✅ |
| نظام الأوامر الموحد (Command Pattern — المرحلة 0) | 127-131 | `ocr-core` ‏src/ocr_core/commands/ + CLI | **رُفع** (v0.7.0) مع إصلاح `ocr.extract` |
| مراجعة Qwen لنظام الأوامر (برومبت) | 131 | `ocr-core` docs/review/qwen_review_prompt_commands.md | **رُفع** |
| قصاصات الخط اليدوي — تصميم + مسودات | 137 | — | تجاوزته المراحل 1-3 |
| كشف الكلمات (المرحلة 1): word_detector/line_grouper/detect.* | 139 | `ocr-core` src/ocr_core/preprocess/ + builtins/detect.py | **رُفع** (+إصلاح NameError numpy) |
| المحرر التفاعلي react-konva (المرحلة 2) | 141 | `intelli-file-manager` | **جزئي**: المستودع يملك BBoxEditor/SnippetPanel بديلًا أنضج؛ أُضيفت القيمة الفريدة فقط (snippet-ops split/merge/RTL + useSnippetHistory undo/redo + اختبارات vitest) — التفاصيل في `intelli-file-manager/docs/snippet-editor-ops.md` |
| تجميع السطور + التصدير (المرحلة 3) | 143 | `intelli-file-manager` src/services/line_aggregator.py + dataset_validator.py + API + LineReviewPanel | **رُفع** (المُصدِّر parquet تجاوزه HFExporter JSONL الموجود) |
| محرك jina-ocr-v1 (المرحلة 4) | 145, 149 | `ocr-core` engines/jina_vlm.py + vlm_ocr.* + 39 اختبارًا + docs | **رُفع** (+إصلاح فحص المسار المبكر؛ الأوزان CC BY-NC 4.0 معزولة في extras) |
| حزمة التسليم (برومبت Qwen + مانيفست + تسلسل اختبار) | 151 | `marathon-suite` docs/handoff/ | **رُفع** (هذا المجلد) |

## مبادئ التدقيق المطبقة على الحزمة

1. **لا رفع دون تشغيل**: كل كود Python رُفع بعد `pytest` فعلي (485+68 اختبارًا).
2. **العقد الفعلي لا المفترض**: كود المحادثة افترض واجهات (`OCRProcessor.process(path)`،
   extras `[rapid,arabic,fuzzy]`) غير موجودة — صُححت إلى العقود الحقيقية.
3. **لا تكرار**: ما تجاوزه المستودع بتنفيذ أنضج لم يُزد موازيًا؛ وُثّق القرار.
4. **سياسة الثقة**: ‏`0.0 = مجهولة` محفوظة في كل مسار جديد (دمج، تقسيم، VLM).
5. **عزل التراخيص**: أوزان jina-ocr-v1 ‏(CC BY-NC 4.0) في extra منفصل خارج `[all]`.
