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
    assert st["telegram_total"] == 88          # كلها نشطة بعد ربط بحث 2026-10-07
    assert st["telegram_active"] == 88         # 86 ماراثون + قناتان مربوطتان (3718bea)
    assert st["web_total"] >= 3               # createdres + noor + medlineplus


def test_translation_registry_matches_forwarder_seed():
    """سجل المصادر يعكس بذرة المحرك المخصص translation_harvest.py
    (43 مصدراً مزروعاً) + سجل الماراثون الموثق — كلها active بعد الربط.
    أي انحراف يعني أن السجل صار أقدم من المحرك — راجع README/التحديث."""
    c = Campaign.load(TRANS_DIR)
    st = c.stats()
    assert len(c.telegram_sources) == 88
    assert st["telegram_active"] == 88
    assert st["telegram_total"] - st["telegram_active"] == 0  # لا pending_wiring
    wired = [s for s in c.telegram_sources
             if s.name in ("medicalrefrencess", "medicalegypt")]
    assert len(wired) == 2
    for s in wired:
        assert s.ingest_status == "active"
        assert "wired_verified" in s.extra


def test_translation_executor_binding_points_to_dedicated_engine():
    """المنفّذ هو المحرك المخصص في gdrive-telegram-tools (3718bea)."""
    c = Campaign.load(TRANS_DIR)
    assert c.executor["repo"] == "gdrive-telegram-tools"
    assert "translation_harvest" in c.executor["path"]
    assert "sent_index" in c.executor.get("dedup_ledger", "")
    assert "translation_harvest" in c.executor.get("state", "")
    assert "migrate" in c.executor.get("seeding", "")


def test_translation_no_internal_ids_leak():
    c = Campaign.load(TRANS_DIR)
    for s in (*c.telegram_sources, *c.web_sources):
        assert "access_hash" not in s.extra
        if str(s.extra.get("ref", "")).startswith("tg_id:"):
            assert s.address  # عنوان السحب متاح رغم غياب handle