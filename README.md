# marathon-suite

المنسّق الخفيف لمنظومة الماراثون — **coordinator، وليس monorepo**.

لا يكرر أي كود من النواتين. دوره: تثبيت الإصدارات المتوافقة، امتلاك
عقد الجسر بين النواتين، وبوابة تكامل حقيقية تُشغَّل على النواتين
المثبتتين من وسومهما.

## خريطة المنظومة

| المستودع | الدور | الإصدار المثبَّت هنا |
|---|---|---|
| [ocr-core](https://github.com/DrAbdulmalek/ocr-core) | مصدر حقيقة OCR: قواعد/charter، محركات، preprocessing، benchmarks | `v0.4.0` |
| [translation-core](https://github.com/DrAbdulmalek/translation-core) | مصدر حقيقة الترجمة: سجل لغات، محركات، جودة، A/B، TM/TMX، مسرد | `v0.1.0` |
| **marathon-suite** (هذا المستودع) | تثبيت الإصدارات + عقد الجسر + بوابة تكامل | `v0.1.0` |
| [marathon_ted_pipeline](https://github.com/DrAbdulmalek/marathon_ted_pipeline) | التطبيق المستهلك (ينقر الـpins الخاصة به) | — |

## عقد الجسر (bridge.py)

```python
from marathon_suite import build_translation_plan
from ocr_core.rtl_utils import ArabicRTLFixer
from translation_core.tm import TranslationMemory
from translation_core.glossary import Glossary

plan = build_translation_plan(
    ocr_text="مالسلا مكيلع",
    tm=TranslationMemory(path="memory.jsonl"),
    glossary=Glossary(path="glossary.yaml"),
)
plan.ocr_text        # "عليكم السلام" — أُصلح RTL قبل البحث
plan.tm_hit          # مباراة تامة/ضبابية مع score محسوب
plan.needs_human     # سياسة صادقة: بلا مباراة تامة → بشري
```

سياسة الثقة في الجسر:
- المباراة **التامة** فقط تُعتمد آليًا؛ الضبابية تُعرض باحتمالها المحسوب.
- بلا مباراة تامة → `needs_human=True` — **لا ترجمة تُختلق**.
- خرائق المسرد تُبلَّغ للمراجع ولا تُصحَّح صامتة.

## التثبيت

```bash
pip install -e .          # يسحب النواتين من وسومهما عبر git
pip install -e ".[dev]"   # + pytest
```

## الترقية بين الإصدارات

ترقية النواة = سطر واحد في `pyproject.toml` (الوسم الجديد) + PR:
بوابة التكامل هنا تختبر التوافق فعليًا قبل أي مستهلك يترقية.
