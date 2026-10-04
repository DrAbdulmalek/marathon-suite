"""عقد الجسر بين ocr-core وtranslation-core — رفيع بلا منطق ثقيل.

التدفق المعتمد:
    نص OCR خام
      → ArabicRTLFixer (ocr-core): تطبيع أشكال العرض + إصلاح انعكاس بصري
      → TranslationMemory.lookup (translation-core): مباراة تامة؟ ضبابية؟
      → Glossary.detect (translation-core): مصطلحات تحتاج فرضًا
      → TranslationPlan: خطة صريحة للمراجع البشري أو لخط النشر

سياسة الثقة (نفس روح النواتين):
- المباراة التامة فقط تُعتمد آليًا؛ الضبابية تُعرض باحتمالها المحسوب.
- بلا مباراة تامة → needs_human=True — **لا ترجمة تُختلق**.
- خرائق المسرد تُبلَّغ ولا تُصحَّح صامتة.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ocr_core.rtl_utils import ArabicRTLFixer
from translation_core.glossary import Glossary
from translation_core.tm import TranslationMemory


@dataclass
class TranslationPlan:
    """خطة ترجمة صريحة: ماذا نعرف، ماذا اقترحنا، وماذا يحتاج بشريًا."""

    ocr_text: str                       # بعد إصلاح RTL
    rtl: Dict = field(default_factory=dict)
    tm_hit: Optional[Dict] = None       # {"target", "score", "kind"}
    glossary_terms: List[Dict] = field(default_factory=list)
    needs_human: bool = True            # الافتراضي الصادق: بلا دليل → بشري

    def asdict(self) -> Dict:
        return {
            "ocr_text": self.ocr_text,
            "rtl": self.rtl,
            "tm_hit": self.tm_hit,
            "glossary_terms": self.glossary_terms,
            "needs_human": self.needs_human,
        }


def build_translation_plan(ocr_text: str,
                           tm: TranslationMemory,
                           glossary: Glossary,
                           rtl_fixer: Optional[ArabicRTLFixer] = None,
                           fuzzy_fallback: bool = False) -> TranslationPlan:
    """يبني خطة ترجمة من نص OCR عبر النواتين — بلا قرارات صامتة.

    الخطوات:
    1. إصلاح RTL إن كان النص عربيًا (تطبيع أشكال العرض + إصلاح انعكاس
       بصري عند تجاوز العتبة) — من ocr-core.
    2. بحث الذاكرة: مباراة تامة (score=1.0) تعتمد آليًا؛ الضبابية تُعرض
       فقط إذا سُمح بها (fuzzy_fallback) وتبقى needs_human=True.
    3. اقتراحات المسرد من النص المُصلَح.
    """
    fixer = rtl_fixer or ArabicRTLFixer()
    text = ocr_text or ""
    rtl_stats: Dict = {"contains_arabic": fixer.contains_arabic(text)}

    if rtl_stats["contains_arabic"]:
        rtl_stats["reversal_ratio"] = round(fixer.reversal_ratio(text), 4)
        fixed = fixer.fix_text(text)
        rtl_stats["changed"] = fixed != text
        text = fixed

    plan = TranslationPlan(ocr_text=text, rtl=rtl_stats)

    matches = tm.lookup(text, fuzzy=False)  # التامة فقط للاعتماد الآلي
    if matches:
        m = matches[0]
        plan.tm_hit = {"target": m.unit.target, "score": m.score,
                       "kind": m.kind}
        plan.needs_human = False
    elif fuzzy_fallback:
        fuzzy = tm.lookup(text, fuzzy=True)
        if fuzzy:
            plan.tm_hit = {"target": fuzzy[0].unit.target,
                           "score": fuzzy[0].score,
                           "kind": fuzzy[0].kind}
            plan.needs_human = True  # ضبابية = اقتراح لا اعتماد

    plan.glossary_terms = glossary.suggest(text)
    return plan
