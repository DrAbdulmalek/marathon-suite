"""marathon_suite — المنسّق الخفيف للمنظومة.

ليس monorepo: لا يكرر كودًا من النواتين. دوره ثلاثة:
1. **تثبيت الإصدارات**: pyproject يثبّت ocr-core@v0.4.0 وtranslation-core@v0.1.0
   بالوسوم — مصدر حقيقة واحد لمجموعة التوافق.
2. **عقد الجسر**: bridge.py يعرّف كيف يتدفق النص بين النواتين
   (OCR → إصلاح RTL → ذاكرة الترجمة → مسرد → خطة للمراجع).
3. **بوابة تكامل**: اختبارات حقيقية تُشغَّل على النواتين المثبتتين
   فعليًا من وسومهما — أي كسر توافق يُرى هنا قبل أن يصل للمستهلكين.
"""
from .bridge import TranslationPlan, build_translation_plan

__version__ = "0.1.0"

__all__ = ["TranslationPlan", "build_translation_plan", "__version__"]
