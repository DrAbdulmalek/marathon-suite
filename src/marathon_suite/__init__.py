"""marathon_suite — المنسّق الخفيف للمنظومة.

ليس monorepo: لا يكرر كودًا من النواتين. دوره ثلاثة:
1. **تثبيت الإصدارات**: pyproject يثبّت ocr-core@v0.4.0 وtranslation-core@v0.1.0
   بالوسوم — مصدر حقيقة واحد لمجموعة التوافق.
2. **عقد الجسر**: bridge.py يعرّف كيف يتدفق النص بين النواتين
   (OCR → إصلاح RTL → ذاكرة الترجمة → مسرد → خطة للمراجع).
3. **بوابة تكامل**: اختبارات حقيقية تُشغَّل على النواتين المثبتتين
   فعليًا من وسومهما — أي كسر توافق يُرى هنا قبل أن يصل للمستهلكين.
"""
# صادرات كسولة (PEP 562): تحميل الحملات لا يتطلب النواتين المثبّتَين؛
# الجسر يُستورد عند أول لمسة فقط (بيئة التكامل حيث ocr-core وtranslation-core جاهزان).
__all__ = ["TranslationPlan", "build_translation_plan",
           "Campaign", "CampaignError", "Source", "__version__"]


def __getattr__(name: str):
    if name in ("TranslationPlan", "build_translation_plan"):
        from .bridge import TranslationPlan as _TP, build_translation_plan as _btp
        return {"TranslationPlan": _TP,
                "build_translation_plan": _btp}[name]
    if name in ("Campaign", "CampaignError", "Source"):
        from . import campaign as _c
        return getattr(_c, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
