# فرز طلبات الدمج — الدفعة 2 (S1-T4 استكمالًا، التالية الأقدم 30 بعد الدفعة 1)

> التاريخ: 2026-10-08 | الأسلوب: نفس منهجية الدفعة 1، مبنيًا على الحالة الحية وقت الفرز.
> **القاعدة الحاكمة:** 123 رقم أساس تاريخي لا رقم ثابت — المصالحة الحية أدناه هي المرجع.
> التصنيف على مستوى إشارات API (CI + قابلية الدمج + الأساس + المسودة)؛ **لا دمج لأي بند
> قبل مراجعة بشرية للـ diff** وفق العقد §2-Level C.

## المصالحة الحية (reconciliation)

| القياس | الأساس (2026-10-08 صباحًا) | الحية عند هذا الفرز |
|---|---|---|
| PRs مفتوحة في المحفظة كلها | 123 | **131** |
| PRs مفتوحة في omni-medical-suite | 43 | **44** |

الأرقام تتغير مع كل دمج/إغلاق/فتح — تُعاد المصالحة في كل دفعة.

## ملخص الدفعة 2

| التصنيف | العدد |
|---|---|
| SAFE_TO_MERGE (مرشح — مراجعة diff إلزامية) | 9 |
| NEEDS_REWORK | 3 |
| DEFER (مسودة/مكدَّس/CI جارٍ) | 2 |
| CLOSE | 0 |

## الجدول التفصيلي (30 طلبًا)

| # | العنوان | الأساس | CI | mergeable | التصنيف | السبب/الدليل |
|---|---|---|---|---|---|---|
| 155 | chore(deps): bump actions/setup-python from 5 to 7 | `main` | أخضر 25/25 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 156 | chore(deps): bump actions/setup-java from 4 to 6 | `main` | أخضر 22/22 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 157 | chore(deps): bump actions/cache from 4 to 6 | `main` | فاشل 2/22: Matrix Summary, HF Space Docker build | unknown | **NEEDS_REWORK** | CI أحمر |
| 158 | chore(deps): update gradio requirement from <5.0.0,>=4.44.0 to >=4.44. | `main` | فاشل 1/25: test (3.12) | unknown | **NEEDS_REWORK** | CI أحمر |
| 159 | chore(deps): update huggingface-hub requirement from <1.0.0,>=0.19.0 t | `main` | أخضر 26/26 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 160 | chore(deps): update filelock requirement from >=3.31.0 to >=4.0.9 | `main` | أخضر 26/26 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 161 | chore(deps): update sqlalchemy requirement from >=2.0.51 to >=2.0.54 | `main` | أخضر 26/26 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 162 | refactor: consolidate T3/T4/F16 safely on current main | `main` | أخضر 25/25 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 163 | fix: remove nonexistent Dependabot label | `main` | أخضر 22/22 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 164 | Harness Engineering v2.0 — عقد الوكلاء + بوابات التحقق + الذاكرة (مسود | `main` | أخضر 21/21 | unknown | **DEFER** | مسودة |
| 166 | feat(telegram-ocr): استوديو OCR لتيليجرام + تعلم الأنماط/القصاصات + قا | `main` | أخضر 25/25 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |
| 168 | feat(ocr): ABBYY FineReader teacher pipeline (tools/abbyy_teacher) | `main` | فاشل 2/22: Matrix Summary, HF Space Docker build | unknown | **NEEDS_REWORK** | CI أحمر |
| 179 | feat(ocr): enforce OCR truth and training-data review gates | `main` | فاشل 6/25: Matrix Summary, Verify hf-space ↔ app/services mirror, Python 3.10 on Ubuntu | unknown | **DEFER** | مسودة |
| 183 | [SPRINT-1][S1-T5] add secret gate — diff-based credential scan on PRs  | `main` | أخضر 23/23 | unknown | **SAFE_TO_MERGE** | أخضر + أساس main (دليل على مستوى API فقط — راجع الـ diff قبل أي دمج؛ mergeable_state=unknown) |

## ملاحظات تنفيذية

- السلاسل المكدسة على فروع `gs/*` (تظهر في عمود الأساس) تُدمج كاملة كسلسلة أو يُعاد تأسيسها
  على main — القرار لصاحب السلسلة؛ لا تُصنَّف فردية SAFE_TO_MERGE أبذًا وهي مكدسة.
- بنود SAFE_TO_MERGE تبقى **READY_FOR_MERGE** فقط: الدمج نفسه يحتاج تفويضًا صريحًا
  (OD-004 في owner-decision-queue.md).
- الدفعة 3 (الـ30 التالية) تُنفَّذ آليًا في Sprint 3 وفق العقد دون انتظار.
