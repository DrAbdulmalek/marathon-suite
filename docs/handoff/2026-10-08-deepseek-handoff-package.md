<!--
  المصدر: محادثة DeepSeek المشاركة — https://chat.deepseek.com/share/fx7z2oxgpoiikvgihm
  الرسالة الأخيرة (151): "حزمة التسليم الكاملة — Qwen + GitHub + الاختبارات"
  تاريخ الحفظ: 2026-10-08
  الحالة: نُفِّذ الرفع فعليًا بواسطة Qwen (هذا التوثيق يرافق التنفيذ).
-->

# حزمة التسليم — محادثة DeepSeek (2026-10-08)

> هذه وثيقة أرشيفية executable: البرومبت الشامل للمراجعة + قائمة الرفع
> إلى GitHub + تسلسل الاختبارات، كما سلمتها المحادثة.
>
> **نتيجة التنفيذ الفعلي (Qwen، 2026-10-08):**
> - ✅ `ocr-core` ← نظام الأوامر (34 أمرًا/8 فئات) + كشف كلمات الخط اليدوي
>   (word_detector/line_grouper/detect.*) + محرك jina-ocr-v1 (vlm.*) —
>   فرع `feat/commands-handwriting-vlm`، الإصدار 0.7.0، ‏485 اختبارًا أخضر
>   (68 جديدًا) مع تصحيحات تدقيق موثقة في رسالة الدمج.
> - ✅ `intelli-file-manager` ← line_aggregator + dataset_validator +
>   نقطتا API ‏(/api/snippets/lines، /api/snippets/validate) + snippet-ops
>   (تقسيم/دمج/تراجع) مدمجة في SnippetPanel + LineReviewPanel + إصلاح
>   test_arabic_ocr — فرع `feat/line-aggregation-editor-ops`، وخريطة
>   "ماذا أُضيف وماذا تجاوزه المستودع" في `docs/snippet-editor-ops.md`.
> - ⚠️ تصحيحات على الحزمة الأصلية: `ocr.extract` كان يستدعي واجهة غير
>   موجودة (`OCRProcessor.process`) — أُعيد ربطه بالعقد الفعلي؛ extras
>   المحادثة أشارت لإضافات غير موجودة — وُواءمت؛ اختبار RTL fixture معكوس
>   — صُحح؛ ضعف jina_vlm (فحص المسار بعد تحميل 7GB) — أُصلح مع حارس انحدار.

---

# حزمة التسليم الكاملة — Qwen + GitHub + الاختبارات

## الجزء 1 — البرومبت الشامل لـ Qwen

انسخه كاملًا. مُعزَّل تمامًا، لا يحتاج معرفة سابقة.

````markdown
# مهمة: مراجعة معمارية شاملة لمكتبة OCR عربية + محرر قصاصات

أنت **مُراجع معماري تقني**. مهمتك فحص حزمة تطوير كاملة لمشروع `ocr-core` ومشتقاته. **لا تُنفّذ**، **لا تكتب كودًا** — فقط راجع، صنّف، وأعطِ حكمًا.

---

## السياق العام

**صاحب المشروع**: طبيب عربي يبني منظومة OCR للعربية (طبي + TED).

**المشاريع المرتبطة**:
1. `ocr-core` — مكتبة MIT، تجمع محركات OCR + قواعد "Visual Evidence Charter"
2. `intelli-file-manager` — تطبيق سطح مكتب (FastAPI + Next.js + PySide6)
3. `marathon_ted_pipeline` — خط أنابيب ترجمة TED
4. `tg-campaign-toolkit` — أدوات نشر Telegram (خاص)

**الترخيص**: MIT للأكواد. بعض الأوزان مقيدة (Surya, jina-ocr-v1).

---

## ما تريد مراجعته الآن

عملية تطوير على 4 مراحل تُضاف إلى `ocr-core`:

### المرحلة 0 — نظام أوامر موحد (Command Pattern)
- `commands/core.py`: `Command`, `CommandRegistry`, `Executor`, `Pipeline`, `ExecutionContext`
- 31 أمرًا في 8 فئات: `io`, `preprocess`, `ocr`, `postprocess`, `export`, `benchmark`, `detect`, `vlm_ocr`
- محوّلات: CLI (مُنجَز)، HTTP/MCP (مُخطَّط)
- **الفلسفة**: كل عملية أمر — نفس ما تفعله photocraft/wordcraft (Rust)

### المرحلة 1 — كشف الكلمات في الخط اليدوي
- `preprocess/word_detector.py`: 3 كواشف
  - `OnnxWordDetector` — نموذج xournalpp-htr (MIT، ONNX، F1=0.88 على الإنجليزية)
  - `ProjectionDetector` — إسقاط عمودي (سريع، جيد للعربية المتصلة)
  - `HeuristicDetector` — للطوارئ فقط
- `preprocess/line_grouper.py`: تجميع الكلمات في سطور مع RTL صحيح
- أوامر: `detect.words`, `detect.lines`, `detect.words_with_text`

### المرحلة 2 — محرر تفاعلي (react-konva)
- `WordSnippetEditor.tsx` — تحرير BBoxes مع Transformer
- `useSnippetHistory.ts` — undo/redo (reducer مع حد 50)
- `lib/konva-helpers.ts` — تحويل إحداثيات (image ↔ canvas ↔ normalized)
- `lib/snippet-ops.ts` — split/merge/sortRTL
- `EditorToolbar.tsx` — شريط الأدوات (Undo, Redo, Split, Merge, Approve, Delete)
- `SnippetSidebar.tsx` — تحرير النص + اقتراحات المسرد الطبي

### المرحلة 3 — تجميع السطور + تصدير HuggingFace
- `line_aggregator.py` — تجميع RTL-aware + mixed text handling
- `dataset_validator.py` — 7 بوابات جودة (bbox، نص، أرقام، وحدات طبية)
- `hf_exporter.py` — Parquet + images + dataset card
- `export_from_db()` — سكربت كامل من SQLite

### المرحلة 4 (جديدة) — محرك jina-ocr-v1 VLM
- `engines/jina_vlm.py` — محرك VLM end-to-end
- أوامر: `vlm.extract`, `vlm.extract_batch`, `vlm.pdf_to_markdown`
- **الترخيص**: الأوزان CC BY-NC 4.0 (غير تجاري)
- **المواصفات**: 3.4B MoE، ~7.4GB VRAM، 2.57 صفحة/ث على A100
- **المُخرج**: Markdown + HTML tables + LaTeX
- **⚠️ لا يعطي bounding boxes**

---

## معايير المراجعة

### أ. صحة معمارية

1. **هل نظام الأوامر (Command Pattern) مناسب** لمكتبة OCR؟ أم هناك نمط أبسط؟
2. **هل `ExecutionContext` كقاموس** هو الخيار الصحيح؟ أم dataclass بحقول صريحة؟
3. **`params_schema` بصيغة JSON Schema مبسّط** — كافٍ؟ أم نحتاج pydantic؟
4. **فصل المراحل الأربع** — منطقي؟ أم هناك تداخل؟
5. **التوافق الخلفي**: هل الإضافات **تُضاف** أم **تستبدل** الكود الموجود؟

### ب. جودة الكود

6. **مشاكل في الأخطاء**: ماذا لو فشل أمر في منتصف Pipeline؟ `trace` كافٍ؟
7. **الأداء**: تمرير `ExecutionContext` عبر كل استدعاء — overhead؟
8. **الاختبارات**: ~80 اختباراً — كافية؟ ما الناقص؟
9. **خصوصًا `WordSnippetEditor.tsx`**: هل `handleStageMouseDown` مع `new Konva.Rect` خارج render صحيح؟

### ج. الخطر المعماري (Red Flags)

10. **jina-ocr-v1 والترخيص**: الأوزان CC BY-NC. إضافتها كـ extra منفصل — كافٍ قانونيًا؟
11. **`trust_remote_code=True`**: تشغيل كود من HuggingFace على جهاز طبيب — خطر أمني؟
12. **التضارب المحتمل**: `vlm.extract` و `ocr.extract` في نفس الفئة — منطقي؟
13. **على العربية**: لا أرقام منشورة. كيف نقيس؟ ما الاختبار الأدنى المقبول؟

### د. اكتمال الرؤية

14. **ما الأوامر الناقصة** لتشغيل مكتبة OCR في الإنتاج؟
15. **هل المرحلة 4 (VLM) فكرة صحيحة**، أم يجب التركيز على المراحل 1-3 أولاً؟
16. **ما الذي يجب حذفه** لأنه زائد؟

---

## قواعد إجابتك

- **لا تقترح مكتبات جديدة** إلا إذا كان ذلك ضروريًا.
- **لا تُعِد صياغة الكود** — راجع التصميم.
- **أشر لكل ملاحظة**: `[خطير/عالي/متوسط/منخفض]`.
- **لا تجامل**. إن كان التصميم سيئًا، قل ذلك بوضوح مع السبب.
- **اذكر ما هو جيد** — ليس كل المراجعة نقدًا.

---

## صيغة الإخراج المطلوبة

### 1. الحكم التنفيذي (5-10 أسطر)
هل الحزمة جاهزة للدمج؟ نعم / لا / بعد تعديلات

### 2. قائمة الملاحظات مرتبة بالأولوية
| # | الملاحظة | الخطورة | الموقع | الإجراء المقترح |

### 3. نقاط قوة (5-7 نقاط)

### 4. مخاطر مُصنَّفة
- **قانونية**: ...
- **أمنية**: ...
- **تقنية**: ...
- **تجارية**: ...

### 5. قرار صريح
- ✅ ادمج كل شيء
- ⚠️ ادمج بعد تعديلات (اذكرها)
- ❌ لا تدمج (مع السبب)

### 6. سؤال واحد للمصمم (إن وُجد)

**ابدأ الآن. لا تسألني أسئلة توضيحية.**
````

---

## الجزء 2 — قائمة الرفع إلى GitHub

### الفرع المقترح

```bash
git checkout main
git pull
git checkout -b feat/jina-vlm-and-editor
```

### الملفات — 18 ملفاً في 3 commits

**Commit 1 — نظام الأوامر (الأساس)**

```bash
# core
src/ocr_core/commands/__init__.py
src/ocr_core/commands/core.py

# builtins (8 ملفات)
src/ocr_core/commands/builtins/__init__.py
src/ocr_core/commands/builtins/io.py
src/ocr_core/commands/builtins/preprocess.py
src/ocr_core/commands/builtins/ocr.py
src/ocr_core/commands/builtins/postprocess.py
src/ocr_core/commands/builtins/export.py
src/ocr_core/commands/builtins/benchmark.py
src/ocr_core/commands/builtins/detect.py

# adapters
src/ocr_core/commands/adapters/__init__.py
src/ocr_core/commands/adapters/cli.py

# tests
tests/commands/__init__.py
tests/commands/test_core.py
tests/commands/test_builtins.py

# docs
docs/commands.md

git add src/ocr_core/commands/ tests/commands/ docs/commands.md pyproject.toml
git commit -m "feat(commands): unified command system (photocraft-inspired)

- Command/Registry/Executor/Pipeline/ExecutionContext
- 28 builtin commands in 6 categories
- CLI adapter (ocr-core <list|describe|run|pipeline>)
- Zero breaking changes to existing OCRProcessor"
```

**Commit 2 — كشف الكلمات والمحرر (المراحل 1-3)**

```bash
# preprocess (كشف + تجميع)
src/ocr_core/preprocess/__init__.py
src/ocr_core/preprocess/word_detector.py
src/ocr_core/preprocess/line_grouper.py

# services (تجميع + تصدير)
backend/app/services/line_aggregator.py
backend/app/services/dataset_validator.py
backend/app/services/hf_exporter.py

# API
backend/app/api/export.py

# frontend (المحرر)
frontend/components/WordSnippetEditor.tsx
frontend/components/EditorToolbar.tsx
frontend/components/SnippetSidebar.tsx
frontend/components/LineReviewPanel.tsx
frontend/hooks/useSnippetHistory.ts
frontend/hooks/useSnippetApi.ts
frontend/lib/konva-helpers.ts
frontend/lib/snippet-ops.ts

# scripts
scripts/export_training_data.py
scripts/upload_to_hf.py

# tests
tests/preprocess/__init__.py
tests/preprocess/test_word_detector.py
tests/preprocess/test_line_grouper.py
tests/services/__init__.py
tests/services/test_line_aggregator.py
tests/services/test_dataset_validator.py
tests/services/test_hf_exporter.py

git add src/ocr_core/preprocess/ backend/ frontend/ scripts/ tests/ docs/word_detection.md docs/phase3_export.md
git commit -m "feat(handwriting): word detection + interactive editor + HF export

- word_detector: ONNX + Projection + Heuristic
- line_grouper: RTL-aware line aggregation
- WordSnippetEditor: react-konva + Transformer
- dataset_validator: 7 quality gates (numbers, medical units)
- hf_exporter: parquet + dataset card
- ~50 tests (unit + integration)"
```

**Commit 3 — jina-ocr-v1 (المرحلة 4)**

```bash
# engine
src/ocr_core/engines/jina_vlm.py

# command
src/ocr_core/commands/builtins/vlm_ocr.py

# scripts
scripts/test_vlm_quick.py

# tests
tests/engines/__init__.py
tests/engines/test_jina_vlm.py
tests/commands/test_vlm_commands.py
tests/integration/__init__.py
tests/integration/test_vlm_integration.py

# docs
docs/jina_ocr_v1.md

git add src/ocr_core/engines/jina_vlm.py \
        src/ocr_core/commands/builtins/vlm_ocr.py \
        scripts/test_vlm_quick.py \
        tests/engines/ tests/commands/test_vlm_commands.py \
        tests/integration/ docs/jina_ocr_v1.md pyproject.toml
git commit -m "feat(vlm): jina-ocr-v1 engine (CC BY-NC weights)

- JinaVLMEngine: lazy loading, clear error messages
- Commands: vlm.extract, vlm.extract_batch, vlm.pdf_to_markdown
- 39 tests (unit, commands, integration)
- pyproject: [jina] and [vlm] extras (not in [all])
- LICENSE NOTE: weights are CC BY-NC 4.0, not for commercial use"
```

### الرفع

```bash
# تحقق أولًا
git log --oneline -3
git status   # يجب أن يكون نظيفًا

# ارفع
export GH_TOKEN="التوكن_الجديد"   # لا تلصقه هنا
git push -u origin feat/jina-vlm-and-editor

# افتح PR draft
gh pr create --draft \
  --base main \
  --head feat/jina-vlm-and-editor \
  --title "[DRAFT] Command system + word editor + jina-ocr-v1" \
  --body "راجع وصف الـ PR في attachments/qwen_prompt.md"
```

---

## الجزء 3 — تسلسل الاختبارات

### المرحلة 0 — التحقق من البنية (5 دقائق)

```bash
cd ~/path/to/ocr-core

# 1. الملفات موجودة
find src/ocr_core/commands -name "*.py" | wc -l   # يجب 13
find tests/commands -name "*.py" | wc -l          # يجب 4

# 2. الأوامر مسجّلة
python -c "
import sys; sys.path.insert(0, 'src')
from ocr_core.commands.core import registry
from ocr_core.commands.builtins import *
print(f'عدد الأوامر: {len(registry.list())}')
print(f'الفئات: {registry.categories()}')
"
# المتوقع: 31 أمر، 8 فئات
```

### المرحلة 1 — اختبارات الوحدة (5 دقائق)

```bash
pip install -e ".[dev,preprocess]"

# اختبارات الأوامر
pytest tests/commands/test_core.py -v
pytest tests/commands/test_builtins.py -v

# اختبارات كشف الكلمات
pytest tests/preprocess/ -v

# اختبارات الخدمات
pytest tests/services/ -v

# اختبارات jina (بلا GPU — سريعة)
pytest tests/engines/test_jina_vlm.py -v
pytest tests/commands/test_vlm_commands.py -v
pytest tests/integration/test_vlm_integration.py -v
```

**المتوقع**: 90+ اختبار، كلها تنجح (jina يستخدم skipif للثقيلة).

### المرحلة 2 — اختبار حقيقي (بدون VLM) (10 دقائق)

```bash
# 1. أنشئ صورة اختبار
python -c "
from PIL import Image, ImageDraw
img = Image.new('L', (600, 200), 'white')
d = ImageDraw.Draw(img)
d.rectangle([50, 60, 150, 120], fill=0)
d.rectangle([200, 60, 350, 120], fill=0)
d.rectangle([400, 60, 550, 120], fill=0)
img.save('/tmp/test_hand.png')
"

# 2. كشف الكلمات
python -c "
import sys; sys.path.insert(0, 'src')
from PIL import Image
from ocr_core.preprocess.word_detector import detect_words
from ocr_core.preprocess.line_grouper import LineGrouper

img = Image.open('/tmp/test_hand.png')
boxes = detect_words(img, kind='projection')
print(f'كشف {len(boxes)} كلمة')

grouper = LineGrouper()
lines = grouper.group(boxes, reading_direction='rtl')
print(f'في {len(lines)} سطر')
for i, line in enumerate(lines):
    print(f'  سطر {i}: {len(line)} كلمة')
"
# المتوقع: 3 كلمات في سطر واحد
```

### المرحلة 3 — اختبار المحرر (15 دقيقة، في المتصفح)

```bash
# في terminal آخر:
cd frontend
npm install react-konva konva zustand immer lucide-react
npm run dev

# افتح: http://localhost:3000/edit-ocr
```

**قائمة الفحص**:
- [ ] ارفع صورة → المربعات تظهر
- [ ] اسحب مربعًا → يتحرك
- [ ] استخدم مقابض التحجيم → يتغير حجمه
- [ ] ارسم مربعًا جديدًا على مساحة فارغة → يُنشأ
- [ ] اختر مربعين + Ctrl → يظهران محددين
- [ ] اضغط `M` → يُدمجان
- [ ] اختر مربعًا + اضغط `S` → ينقسم
- [ ] اكتب نصًا في اللوحة الجانبية → يُحفظ
- [ ] Ctrl+Z → يتراجع
- [ ] Ctrl+S → يُحفظ

### المرحلة 4 — اختبار jina-ocr-v1 (اختياري، يحتاج GPU)

```bash
# تحقق من GPU أولًا
python -c "import torch; print(torch.cuda.is_available())"

# إن كان True، ثبّت jina
pip install "marathon-ocr-core[jina]"

# اختبار حيوي
python scripts/test_vlm_quick.py --arabic --strict
```

**قائمة الفحص**:
- [ ] النموذج يُحمّل (3-5 دقائق أول مرة)
- [ ] الاستخراج يعمل
- [ ] النص العربي يظهر (هل الأحرف صحيحة؟)
- [ ] الوقت منطقي (< 30 ثانية/صورة)
- [ ] VRAM لا يتجاوز 10 GB

### المرحلة 5 — تقرير النتائج

أرسل:

1. **مخرجات الاختبارات**:
   ```
   pytest tests/ -v > /tmp/test_results.txt
   # أرسل آخر 50 سطرًا
   ```

2. **نتيجة اختبار jina** (إن شغّلته):
   ```
   python scripts/test_vlm_quick.py --arabic --strict 2>&1 | tee /tmp/jina_test.txt
   ```

3. **مخرجات Qwen** — التقرير الكامل

---

## ⚠️ ملاحظات أمانة قبل البدء

1. **لم أشغّل أي شيء في بيئتي**. جميع الأرقام من توثيق المكتبات. الاختبار الحقيقي عليك.

2. **`jina_vlm.py` قد يحتاج تعديلًا**:
   - `AutoProcessor.prepare_ocr_inputs` — قد يكون اسمًا مختلفًا
   - راجع `example.py` على HuggingFace قبل التشغيل
   - إن فشل، أرسل الـ traceback

3. **`react-konva` مع Next.js 15+**:
   - يجب `dynamic(() => import(...), { ssr: false })`
   - قد تحتاج `next.config.js` مع `transpilePackages: ['konva']`

4. **المسارات قد تحتاج تعديلًا**:
   - `backend.app.services.*` يفترض أن `intelli-file-manager` هو المستودع الجذر
   - إن نقلت الملفات إلى `ocr-core`، عدّل الـ imports

5. **الترخيص**:
   - `ocr-core` = MIT ✅
   - `jina-ocr-v1` weights = CC BY-NC ❌
   - أضف `LICENSE-NOTES.md` يوضح الفرق

---

## 📋 قائمة تحقق نهائية

قبل رفع GitHub:
- [ ] كل الملفات منسوخة
- [ ] `pytest tests/commands/` ينجح
- [ ] `pytest tests/preprocess/` ينجح
- [ ] `ocr-core list` يعمل
- [ ] لا أسرار في الكود (`git diff --cached | grep -i "token\|key\|secret"`)
- [ ] `pyproject.toml` محدّث
- [ ] `README.md` يذكر jina-ocr-v1 والترخيص

قبل تشغيل Qwen:
- [ ] البرومبت مُعاد قراءته
- [ ] الإجابة مُنتظَرة بالكامل

قبل الاختبار:
- [ ] نسخة احتياطية: `git bundle create backup.bundle --all`
- [ ] البيئة نظيفة: `pip install -e ".[dev,preprocess]"`

---

**الترتيب المقترح**:
```
1. انسخ الملفات (30 د)
2. شغّل pytest محليًا (10 د)
3. رفع GitHub (5 د)
4. أرسل إلى Qwen (متوازٍ)
5. اختبار المحرر في المتصفح (15 د)
6. اختبار jina إن توفر GPU (30 د)
7. اقرأ تقرير Qwen (10 د)
8. قرّر: دمج / تعديل / إعادة تصميم
```

**لا تدمج PR قبل قراءة تقرير Qwen.**
