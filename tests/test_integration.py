# tests/test_integration.py
"""بوابة تكامل marathon-suite — تُشغَّل على النواتين المثبتتين فعليًا
من وسومهما (v0.4.0 + v0.1.0) لا على نسخ مطورة محليًا.

كل اختبار هنا حقيقي: لا شبكة، لا نماذج، لا محاكاة للنواتين نفسهما.
"""
import importlib.metadata as md

from ocr_core.rtl_utils import ArabicRTLFixer
from ocr_core.rules.engine import OCRProcessor
from translation_core.glossary import Glossary
from translation_core.tm import TranslationMemory

from marathon_suite import build_translation_plan


# ---------- 1. عقود التثبيت: النواتان بالوسوم المتفق عليها ----------
def test_ocr_core_pinned_version():
    assert md.version("marathon-ocr-core") == "0.4.0"


def test_translation_core_pinned_version():
    assert md.version("marathon-translation-core") == "0.1.0"


# ---------- 2. الجانب ocr-core حقيقي ----------
def test_rtl_normalize_presentation_forms():
    """أشكال العرض (مخرجات OCR قديمة) → يونيكود قياسي."""
    f = ArabicRTLFixer()
    assert f.contains_arabic("\uFEDE\uFE8E\uFEB4")
    assert f.normalize_presentation_forms("\uFEDE\uFE8E\uFEB4") == "لاس"


def test_rtl_fix_reverses_visual_arabic():
    f = ArabicRTLFixer()
    assert f.reversal_ratio("السلام عليكم") == 0.0
    assert f.reversal_ratio("مالسلا مكيلع") > 0.0
    assert f.fix_text("مالسلا مكيلع", force=True) == "عليكم السلام"


def test_ocr_processor_default_charter_loads():
    """OCRProcessor() بلا وسائط: ملف القواعد من الحزمة، مستقل عن CWD."""
    p = OCRProcessor()
    assert p.version >= 2
    assert p.config.get("visual_markers") or p.config.get("rules")


# ---------- 3. الجانب translation-core حقيقي ----------
def _tm_with_hit():
    tm = TranslationMemory()
    tm.add("السلام عليكم", "وعليكم السلام ورحمة الله")
    return tm


def _glossary():
    return Glossary(entries={"terms": {
        "dataset": {"target": "مجموعة البيانات",
                    "alt": ["داتاسِت", "قاعدة البيانات"]},
    }})


# ---------- 4. الجسر: التدفق الكامل ----------
def test_plan_exact_tm_hit_is_auto_approved():
    """مباراة تامة في الذاكرة → تُعتمد آليًا (needs_human=False)."""
    plan = build_translation_plan(
        "السلام عليكم", tm=_tm_with_hit(), glossary=_glossary())
    assert plan.rtl["contains_arabic"] is True
    assert plan.tm_hit == {
        "target": "وعليكم السلام ورحمة الله", "score": 1.0, "kind": "exact"}
    assert plan.needs_human is False


def test_plan_without_hit_needs_human():
    """[سياسة] بلا مباراة تامة → بشري. لا ترجمة تُختلق."""
    plan = build_translation_plan(
        "جملة لم تُترجم من قبل إطلاقًا",
        tm=_tm_with_hit(), glossary=_glossary())
    assert plan.tm_hit is None
    assert plan.needs_human is True


def test_plan_fuzzy_fallback_suggests_but_stays_human():
    """الضبابية تُعرض باحتمالها المحسوب ولا تُعتمد — فشل صادق."""
    tm = TranslationMemory(fuzzy_threshold=0.6)
    tm.add("الرئيس ألقى خطابًا أمس في المؤتمر.",
           "ألقى الرئيس خطابًا أمس بالمؤتمر.")
    plan = build_translation_plan(
        "الرئيس ألقى خطابًا أمس في المؤتمر العام.",
        tm=tm, glossary=_glossary(), fuzzy_fallback=True)
    assert plan.tm_hit is not None and plan.tm_hit["kind"] == "fuzzy"
    assert 0.6 <= plan.tm_hit["score"] < 1.0
    assert plan.needs_human is True


def test_plan_rtl_fix_runs_before_tm_lookup():
    """نص OCR معكوس بصريًا: الإصلاح أولًا (تلقائيًا) ثم مباراة تامة."""
    tm = TranslationMemory()
    tm.add("عليكم السلام", "رد التحيّة المعتمد")
    plan = build_translation_plan("مالسلا مكيلع", tm=tm,
                                  glossary=_glossary())
    assert plan.rtl["contains_arabic"] is True
    assert plan.rtl["changed"] is True
    assert plan.ocr_text == "عليكم السلام"      # أُصلح قبل البحث
    assert plan.tm_hit is not None and plan.tm_hit["kind"] == "exact"
    assert plan.tm_hit["target"] == "رد التحيّة المعتمد"


def test_plan_glossary_suggestions_from_fixed_text():
    """مصطلحات المسرد تُكتشف من النص المُصلَح (بعد RTL لا قبله)."""
    tm = TranslationMemory()
    plan = build_translation_plan(
        "The dataset grows.", tm=tm, glossary=_glossary())
    assert plan.needs_human is True
    assert {"term": "dataset", "target": "مجموعة البيانات"} \
        in plan.glossary_terms


def test_plan_asdict_contract():
    """العقد القابل للتسلسل — للمستهلكين (API/webhooks)."""
    import json
    plan = build_translation_plan(
        "السلام عليكم", tm=_tm_with_hit(), glossary=_glossary())
    d = plan.asdict()
    assert json.dumps(d, ensure_ascii=False)  # قابل للتسلسل فعليًا
    assert set(d.keys()) == {
        "ocr_text", "rtl", "tm_hit", "glossary_terms", "needs_human"}
