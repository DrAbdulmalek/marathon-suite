# tests/test_translation_campaign.py — اختبارات حملة الترجمة (@DrMalekDrive)
"""تتحقق من تحميل تعريف حملة الترجمة الحقيقية المشحونة في المستودع
(التي كانت قبلها مبعثرة في سكربتات tg-campaign-toolkit) وربط المنفّذ.
"""
from pathlib import Path

from marathon_suite.campaign import Campaign

REPO_ROOT = Path(__file__).resolve().parents[1]
TRANS_DIR = REPO_ROOT / "campaigns" / "translation"


# ---------- حملة الترجمة الحقيقية المشحونة ----------
def test_translation_campaign_loads():
    c = Campaign.load(TRANS_DIR)
    assert c.name == "translation"
    assert c.target_handle == "@DrMalekDrive"
    assert c.pull_interval_hours >= 1
    assert c.post_mode == "copy_or_forward"
    assert c.dedup_key == ["file_name", "size_bytes"]


def test_translation_registry_shape():
    c = Campaign.load(TRANS_DIR)
    st = c.stats()
    assert st["telegram_total"] >= 80          # 86 في السجل الحالي
    assert st["telegram_active"] >= 80        # نشط بلا عنوان يُخفَّض آلياً — كلها تحمل عناوين
    assert st["web_total"] >= 3               # createdres + noor + medlineplus


def test_translation_registry_matches_forwarder_primary():
    """سجل المصادر يعكس قائمة PRIMARY في tg_forward_to_channel.py (86 مصدراً).
    أي انحراف يعني أن السجل صار أقدم من السكربت — راجع README/التحديث."""
    c = Campaign.load(TRANS_DIR)
    assert len(c.telegram_sources) == 86


def test_translation_executor_binding_points_to_toolkit():
    c = Campaign.load(TRANS_DIR)
    assert c.executor["repo"] == "tg-campaign-toolkit"
    assert "tg_forward_to_channel" in c.executor["path"]
    assert "sent_index" in c.executor.get("dedup_ledger", "")


def test_translation_no_internal_ids_leak():
    c = Campaign.load(TRANS_DIR)
    for s in (*c.telegram_sources, *c.web_sources):
        assert "access_hash" not in s.extra
        if str(s.extra.get("ref", "")).startswith("tg_id:"):
            assert s.address  # عنوان السحب متاح رغم غياب handle
