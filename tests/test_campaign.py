# tests/test_campaign.py — اختبارات حملات الماراثون (بلا شبكة، بلا جلسات)
"""تتحقق من تحميل حملة العظام الحقيقية المشحونة في المستودع + قواعد الصدق
(رفض التعريفات الناقصة، خفض المصادر النشطة بلا عنوان)."""
from pathlib import Path

import pytest

from marathon_suite.campaign import Campaign, CampaignError

REPO_ROOT = Path(__file__).resolve().parents[1]
ORTHO_DIR = REPO_ROOT / "campaigns" / "ortho"


# ---------- 1. حملة العظام الحقيقية المشحونة ----------
def test_ortho_campaign_loads():
    c = Campaign.load(ORTHO_DIR)
    assert c.name == "ortho"
    assert c.target_handle == "@ortho_homs"
    assert c.pull_interval_hours == 6
    assert c.post_mode == "forward_with_attribution"
    assert c.dedup_key == ["source_handle", "message_id"]


def test_ortho_registry_shape():
    c = Campaign.load(ORTHO_DIR)
    st = c.stats()
    assert st["telegram_total"] >= 30          # 38 في السجل الحالي
    assert st["telegram_active"] >= 30         # 36 نشط
    assert st["sub_sources"] >= 5              # D2: 10 مصادر فرعية
    assert st["web_total"] >= 15               # D3: نور + TED + 20 صفحة جامعة
    assert st["excluded"] >= 1                 # قناتان مستبعَدتان موثّقتان


def test_ortho_no_internal_ids_leak():
    """access_hash يبقى خارج السجل المنشور دائمًا؛ مصادر D2 الفرعية تُعرَّف
    بمرجع tg_id (غير حساس بذاته — الوصول يتطلب عضوية محققة في الجلسة)."""
    c = Campaign.load(ORTHO_DIR)
    for s in (*c.telegram_sources, *c.web_sources):
        assert "access_hash" not in s.extra
        if s.extra.get("ref", "").startswith("tg_id:"):
            assert s.extra.get("requires_membership") is True


def test_ortho_web_layer_has_noor_and_ted():
    c = Campaign.load(ORTHO_DIR)
    ids = {s.extra.get("id") for s in c.web_sources}
    assert "noor_library" in ids
    assert "ted_srt" in ids


def test_executor_binding_points_to_toolkit():
    c = Campaign.load(ORTHO_DIR)
    assert c.executor["repo"] == "tg-campaign-toolkit"
    assert "tg_forward_ortho" in c.executor["path"]


# ---------- 2. قواعد الصدق على تعريفات مصطنعة ----------
def _write_minimal_campaign(tmp_path: Path, **overrides):
    sched = {"pull_interval_hours": 6, "dedup_key": ["source_handle", "message_id"],
             "post_mode": "forward_with_attribution"}
    sched.update(overrides.get("schedule", {}))
    target = {"handle": "@demo_target"}
    target.update(overrides.get("target", {}))
    import yaml
    (tmp_path / "campaign.yaml").write_text(yaml.safe_dump({
        "campaign": "demo",
        "target_channel": target,
        "schedule": sched,
        "executor": {"repo": "x", "path": "y"},
    }, allow_unicode=True), encoding="utf-8")


def test_missing_campaign_yaml_raises(tmp_path: Path):
    with pytest.raises(CampaignError):
        Campaign.load(tmp_path)


def test_missing_target_raises(tmp_path: Path):
    _write_minimal_campaign(tmp_path, target={"handle": None})
    (tmp_path / "campaign.yaml").write_text(
        (tmp_path / "campaign.yaml").read_text(encoding="utf-8")
        .replace("handle: null", "title: x"), encoding="utf-8")
    with pytest.raises(CampaignError):
        Campaign.load(tmp_path)


def test_active_source_without_address_downgraded(tmp_path: Path):
    _write_minimal_campaign(tmp_path)
    import yaml
    (tmp_path / "sources.yaml").write_text(yaml.safe_dump({
        "sources": [
            {"name": "no address", "kind": "channel", "ingest_status": "active"},
            {"name": "ok", "kind": "channel", "handle": "@ok",
             "ingest_status": "active"},
        ],
    }, allow_unicode=True), encoding="utf-8")
    c = Campaign.load(tmp_path)
    no_addr = next(s for s in c.telegram_sources if s.name == "no address")
    ok = next(s for s in c.telegram_sources if s.name == "ok")
    assert no_addr.ingest_status == "inactive"
    assert no_addr.extra["downgraded_reason"]
    assert ok.is_active and ok.address == "@ok"


# ---------- 3. الاستحقاق الزمني ----------
def test_due_schedule():
    from datetime import datetime, timezone
    c = Campaign.load(ORTHO_DIR)
    t0 = datetime(2026, 10, 5, 8, 0, tzinfo=timezone.utc)
    assert not c.is_due(now=t0, last_run=t0)             # قبل المرور
    assert c.is_due(now=t0 + __import__("datetime").timedelta(hours=6, seconds=1),
                    last_run=t0)                          # بعد 6 ساعات
    assert c.due_at(t0) == t0 + __import__("datetime").timedelta(hours=6)
