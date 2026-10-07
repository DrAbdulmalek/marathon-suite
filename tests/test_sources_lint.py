# tests/test_sources_lint.py — بوابة فحص لصحة معرفات مصادر الحملتين
"""تمنع دخول معرفات مشوهة إلى السجلات، وتضمن أن كل مصدر pending_wiring
يحمل عنوان سحب وتاريخ تحقق، وكل استبعاد يحمل سبباً — لا اختلاق ولا صمت."""
import re
from pathlib import Path

import pytest

from marathon_suite.campaign import Campaign

REPO_ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_DIRS = {
    "ortho": REPO_ROOT / "campaigns" / "ortho",
    "translation": REPO_ROOT / "campaigns" / "translation",
}
HANDLE_RE = re.compile(r"^@[A-Za-z][A-Za-z0-9_]{3,31}$")


@pytest.mark.parametrize("name", sorted(CAMPAIGN_DIRS))
def test_handles_well_formed(name):
    c = Campaign.load(CAMPAIGN_DIRS[name])
    for s in c.telegram_sources:
        if s.handle:
            assert HANDLE_RE.match(s.handle), (
                f"handle مشوه في سجل {name}: {s.handle!r} ({s.name})"
            )


@pytest.mark.parametrize("name", sorted(CAMPAIGN_DIRS))
def test_pending_wiring_sources_are_verified(name):
    c = Campaign.load(CAMPAIGN_DIRS[name])
    pending = [s for s in c.telegram_sources if s.ingest_status == "pending_wiring"]
    for s in pending:
        assert s.address, f"pending_wiring بلا عنوان سحب: {s.name}"
        assert s.extra.get("last_verified"), (
            f"pending_wiring بلا last_verified: {s.name}"
        )


@pytest.mark.parametrize("name", sorted(CAMPAIGN_DIRS))
def test_web_sources_have_url(name):
    c = Campaign.load(CAMPAIGN_DIRS[name])
    for s in c.web_sources:
        assert s.url, f"مصدر ويب بلا url: {s.name}"


@pytest.mark.parametrize("name", sorted(CAMPAIGN_DIRS))
def test_excluded_entries_have_reason(name):
    c = Campaign.load(CAMPAIGN_DIRS[name])
    for e in c.excluded:
        assert e.get("reason"), "استبعاد بلا سبب موثق: " + str(e.get("name", "?"))