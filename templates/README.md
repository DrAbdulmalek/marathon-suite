# Templates — Harness Engineering

> قوالب قابلة للنسخ لإعداد Harness Engineering في أي مشروع (جديد أو قائم).
> هذا هو التوزيع المركزي في `marathon-suite` — منسّق أسطولة الماراثون.

## ما هو الـ Harness؟

مجموعة الملفات التي تحكم **كيف** يعمل وكيل الذكاء الاصطناعي على مشروعك:
ماذا يفعل، كيف يتحقق، متى يتوقف، وكيف يسلّم للجلسة التالية.

بدون Harness، كل جلسة تبدأ من الصفر. مع Harness، الوكيل يقرأ الحالة
ويعرف أين توقف.

## البنية

```
templates/
├── README.md                    ← هذا الملف
├── AGENTS.md                    ← قالب العقد (خصصه لكل مشروع)
├── feature_list.json            ← قالب قائمة المهام
├── progress.md                  ← قالب سجل الجلسات
├── session-handoff.md           ← قالب تسليم الجلسة
├── scripts/
│   ├── bootstrap.sh             ← يولّد ملفات Harness لمشروع
│   ├── verify.sh                ← بوابة التحقق قبل الالتزام
│   └── session-handoff.py       ← مولّد ملخص الجلسة
├── gitignore.template           ← قواعد تجاهل موحّدة (تُدمج مع الموجود)
└── env.example                  ← نموذج الأسرار (قيم وهمية فقط)
```

والدليل المفهومي الكامل: `docs/HARNESS.md` في كل مستودع، ودليل نقل
المشاريع إلى Harness الموحّد: `docs/migration-guide.md` (هنا).

## الاستخدام السريع

### مشروع جديد من الصفر

```bash
bash templates/scripts/bootstrap.sh \
    --project=my-new-project \
    --type=python \
    --target=/path/to/my-new-project \
    --git

# ثم: راجع AGENTS.md واملأ feature_list.json، ثم:
cd /path/to/my-new-project && ./init.sh
```

### مشروع قائم

```bash
cd /path/to/existing-project

# يضيف المفقود ولا يمسّ الموجود (بلا --force=1):
bash /path/to/marathon-suite/templates/scripts/bootstrap.sh \
    --project="$(basename "$PWD")" \
    --target=. \
    --force=0
```

## أنواع المشاريع (--type)

| النوع | البوابة الافتراضية في init.sh |
|-------|-------------------------------|
| `python` | `pytest tests/ -q` (مع PYTHONPATH=src إن وُجد) |
| `fullstack` | tsc --noEmit عند توفر node_modules |
| `minimal` | بلا بوابة — للتوثيق فقط |

ملاحظة: المشاريع التسعة الأساسية في الأسطولة لها كشف وبوابات مدمجة
في init.sh الموحّد (ocr-core، translation-core، marathon-suite،
tg-campaign-toolkit، channel-ops-dashboard، manjaro-care،
omni-medical-suite، marathon_ted_pipeline، intelli-file-manager).

## الملفات المُولَّدة

- **AGENTS.md** — العقد: يقرأه الوكيل قبل أي إجراء (القواعد الصفرية، البوابات،
  النطاق، الأدوات، الذاكرة، صيغة التقرير). **أهم ملف — خصّصه لكل مشروع.**
- **feature_list.json** — المهام: `id, title, status (pending|in_progress|done|
  blocked), priority, depends_on, acceptance`.
- **progress.md** — سجل تراكمي (الأحدث في الأعلى؛ مدخل لكل جلسة).
- **session-handoff.md** — يُعاد توليده كل جلسة (يُستبدل، لا يُضاف).
- **init.sh** — بوابة الدخول (بداية الجلسة). **scripts/verify.sh** — بوابة
  الجودة (قبل الالتزام). **scripts/session-handoff.py** — التسليم + Mem0.

## قواعد ذهبية

1. لا تخترع مصادر — كل ادعاء يحتاج رابطاً أو يُحذف.
2. الترخيص أولاً — لا GPL/AGPL في نواة MIT.
3. عند فشل بوابة → STOP — لا "أصلح بسرعة".
4. كل commit يحمل مخرجاً حقيقياً — لا "يبدو صحيحاً".
5. الأسرار من `$ENV_VAR` فقط — لا تُكتب في ملفات.

## المراجع

- Learn Harness Engineering (MIT، 15 لغة)
- Mem0 / OpenMemory — الذاكرة طويلة المدى
- LobeHub — فرق الوكلاء
- `docs/HARNESS.md` و`docs/migration-guide.md` في هذا المستودع
