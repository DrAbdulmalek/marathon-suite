"""campaign.py — تحميل حملات الماراثون والتحقق من استحقاقها.

روح المنسّق الخفيف: هذا الوحدة **لا تنفّذ السحب ولا النشر** — تقرأ تعريف
الحملة (campaign.yaml) وسجلات المصادر (sources.yaml / web_sources.yaml)،
تتحقق من تماسكها، وتحسب ما هو مستحق الآن. التنفيذ الفعلي بيد المنفّذ
المعرَّف في الحملة (scripts/ortho/tg_forward_ortho.py في tg-campaign-toolkit).

قواعد الصدق نفسها:
- بلا تعريف سليم → خطأ صريح، لا قيم افتراضية مُختلقة.
- المصدر بلا handle (أو بلا url لطبقة الويب) → ingest_status=inactive إجباريًا
  عند التحميل مع تسجيل السبب — لا صمت.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

REQUIRED_CAMPAIGN_KEYS = (
    "campaign",
    "target_channel",
    "schedule",
    "executor",
)
REQUIRED_SOURCE_KEYS = ("name", "kind", "ingest_status")


class CampaignError(ValueError):
    """تعريف حملة غير متماسك — يُرفض التحميل بدل العيش معه."""


@dataclass
class Source:
    """مصدر واحد (تيليجرام أو ويب) في سجل الحملة."""

    name: str
    kind: str
    ingest_status: str = "inactive"
    handle: Optional[str] = None
    url: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.ingest_status == "active"

    @property
    def address(self) -> Optional[str]:
        """عنوان السحب: handle، أو url، أو tme_link — أو None إن كان معلّقًا."""
        return self.handle or self.url or self.extra.get("tme_link") \
            or self.extra.get("ref")


@dataclass
class Campaign:
    """حملة ماراثون محمّلة ومتحقق منها."""

    name: str
    title: str
    target_handle: str
    pull_interval_hours: int
    dedup_key: List[str]
    post_mode: str
    executor: Dict[str, Any]
    telegram_sources: List[Source] = field(default_factory=list)
    web_sources: List[Source] = field(default_factory=list)
    excluded: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    # ---------- الصانع ----------
    @classmethod
    def load(cls, campaign_dir: Path) -> "Campaign":
        """يحمّل الحملة من مجلد يحوي campaign.yaml (+سجلات المصادر إن وُجدت)."""
        campaign_dir = Path(campaign_dir)
        cpath = campaign_dir / "campaign.yaml"
        if not cpath.is_file():
            raise CampaignError(f"missing campaign.yaml in {campaign_dir}")
        raw = yaml.safe_load(cpath.read_text(encoding="utf-8")) or {}
        missing = [k for k in REQUIRED_CAMPAIGN_KEYS if k not in raw]
        if missing:
            raise CampaignError(f"campaign.yaml missing keys: {missing}")

        sched = raw["schedule"] or {}
        target = raw["target_channel"] or {}
        if not target.get("handle"):
            raise CampaignError("target_channel.handle is required")
        if not sched.get("pull_interval_hours"):
            raise CampaignError("schedule.pull_interval_hours is required")

        def _sources(fname: str) -> List[Source]:
            fpath = campaign_dir / fname
            if not fpath.is_file():
                return []
            doc = yaml.safe_load(fpath.read_text(encoding="utf-8")) or {}
            out: List[Source] = []
            for s in doc.get("sources", []) or []:
                bad = [k for k in REQUIRED_SOURCE_KEYS if k not in s]
                if bad:
                    raise CampaignError(f"{fname}: source missing keys {bad}: "
                                        f"{s.get('name', '?')}")
                out.append(Source(
                    name=s["name"],
                    kind=s["kind"],
                    ingest_status=s.get("ingest_status", "inactive"),
                    handle=s.get("handle"),
                    url=s.get("url"),
                    extra={k: v for k, v in s.items()
                           if k not in ("name", "kind", "ingest_status",
                                        "handle", "url")},
                ))
            return out

        tg = _sources(str(raw.get("sources_file", "sources.yaml")))
        web = _sources(str(raw.get("web_sources_file", "web_sources.yaml")))

        # قاعدة الصدق: مصدر نشط بلا عنوان سحب → يُخفَّض إجباريًا مع السبب.
        for s in (*tg, *web):
            if s.is_active and not s.address:
                s.ingest_status = "inactive"
                s.extra["downgraded_reason"] = "active source without handle/url"

        excl_doc = (campaign_dir / str(raw.get("sources_file", "sources.yaml")))
        excluded: List[Dict[str, Any]] = []
        if excl_doc.is_file():
            doc = yaml.safe_load(excl_doc.read_text(encoding="utf-8")) or {}
            excluded = doc.get("excluded", []) or []

        return cls(
            name=raw["campaign"],
            title=raw.get("title", raw["campaign"]),
            target_handle=target["handle"],
            pull_interval_hours=int(sched["pull_interval_hours"]),
            dedup_key=list(sched.get("dedup_key", [])),
            post_mode=sched.get("post_mode", "forward_with_attribution"),
            executor=raw["executor"] or {},
            telegram_sources=tg,
            web_sources=web,
            excluded=excluded,
            raw=raw,
        )

    # ---------- الاستحقاق ----------
    def due_at(self, last_run: Optional[datetime] = None) -> datetime:
        """الوقت المستحق القادم انطلاقًا من آخر تشغيل (أو الآن إن لم يسبق)."""
        base = last_run or datetime.now(timezone.utc)
        return base + timedelta(hours=self.pull_interval_hours)

    def is_due(self, now: Optional[datetime] = None,
               last_run: Optional[datetime] = None) -> bool:
        """هل الحملة مستحقة للسحب الآن؟ (أول تشغيل = مستحقة فورًا)"""
        if last_run is None:
            return True
        moment = now or datetime.now(timezone.utc)
        return moment >= self.due_at(last_run)

    def active_sources(self, layer: str = "all") -> List[Source]:
        """المصادر النشطة؛ layer: telegram / web / all."""
        pools = {
            "telegram": self.telegram_sources,
            "web": self.web_sources,
        }
        if layer != "all":
            return [s for s in pools[layer] if s.is_active]
        return [s for p in pools.values() for s in p if s.is_active]

    # ---------- التقارير ----------
    def stats(self) -> Dict[str, int]:
        tg_active = sum(1 for s in self.telegram_sources if s.is_active)
        web_active = sum(1 for s in self.web_sources if s.is_active)
        subs = sum(1 for s in self.telegram_sources if s.extra.get("hop"))
        return {
            "telegram_total": len(self.telegram_sources),
            "telegram_active": tg_active,
            "sub_sources": subs,
            "web_total": len(self.web_sources),
            "web_active": web_active,
            "excluded": len(self.excluded),
        }

    def asdict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "target_handle": self.target_handle,
            "pull_interval_hours": self.pull_interval_hours,
            "post_mode": self.post_mode,
            "stats": self.stats(),
        }
