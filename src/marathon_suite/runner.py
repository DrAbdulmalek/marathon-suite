"""runner.py — حلقة تشغيل الحملة: هل حان موعد السحب؟ → نفّذ المنفّذ → سجّل.

روح المنسّق الخفيف تُحفظ: هذه الوحدة **لا تعرف شيئًا عن تيليجرام** — تعرف
الجدولة (من campaign.yaml)، والمنفّذ (أمر خارجي)، وحالة التشغيل (ملف محلي
خارج git). الصدق: لا تنفيذ صامت لما لا يستحق، وكل محاولة تُسجَّل بنتيجتها.

المسار الكامل:
    campaign.yaml (كل 6 ساعات) → runner → tg_forward_ortho.py (منفّذ التوكت)
    → حالة forward-ortho المحلية → تقرير دورة إلى state/runner.json

الاستخدام:
    python -m marathon_suite.runner --campaign campaigns/ortho \\
        --executor "python scripts/ortho/tg_forward_ortho.py" \\
        --state state/ortho-runner.json [--dry-run] [--force] [--budget 90]
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .campaign import Campaign, CampaignError


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class CycleResult:
    """نتيجة محاولة دورة واحدة — تُسجَّل كما هي، نجاحًا كانت أو تخطيًا."""

    action: str                      # ran | skipped_not_due | dry_run | error
    campaign: str
    started_at: str = ""
    finished_at: str = ""
    exit_code: Optional[int] = None
    command: str = ""
    stdout_tail: str = ""
    stderr_tail: str = ""
    next_due: Optional[str] = None
    reason: str = ""
    errors: List[str] = field(default_factory=list)

    def asdict(self) -> Dict[str, Any]:
        return {
            "action": self.action, "campaign": self.campaign,
            "started_at": self.started_at, "finished_at": self.finished_at,
            "exit_code": self.exit_code, "command": self.command,
            "stdout_tail": self.stdout_tail, "stderr_tail": self.stderr_tail,
            "next_due": self.next_due, "reason": self.reason,
            "errors": self.errors,
        }


# ---------- حالة التشغيل (خارج git عمدًا — بيانات تشغيلية) ----------
def load_state(state_path: Path) -> Dict[str, Any]:
    if not Path(state_path).is_file():
        return {"history": []}
    return json.loads(Path(state_path).read_text(encoding="utf-8"))


def save_state(state_path: Path, state: Dict[str, Any]) -> None:
    Path(state_path).parent.mkdir(parents=True, exist_ok=True)
    Path(state_path).write_text(
        json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def last_run_at(state: Dict[str, Any]) -> Optional[datetime]:
    """آخر تشغيل *ناجح* — التخطي لا يُحدّث الموعد (لكنه يُسجَّل في التاريخ)."""
    for rec in reversed(state.get("history", [])):
        if rec.get("action") == "ran" and rec.get("started_at"):
            try:
                return datetime.fromisoformat(rec["started_at"])
            except ValueError:
                continue
    return None


def status(campaign: Campaign, state_path: Path) -> Dict[str, Any]:
    """تقرير حالة بلا تنفيذ — يصلح لجدولة CI كل 6 ساعات (report-only)."""
    state = load_state(Path(state_path))
    lr = last_run_at(state)
    due = campaign.is_due(now=_now(), last_run=lr)
    return {
        "campaign": campaign.name,
        "target": campaign.target_handle,
        "stats": campaign.stats(),
        "last_run": _iso(lr) if lr else None,
        "is_due": due,
        "next_due": _iso(campaign.due_at(lr)) if lr else "now (لم يُشغَّل بعد)",
        "runs_recorded": len(state.get("history", [])),
    }


def run_cycle(campaign_dir: Path,
              executor_cmd: str,
              state_path: Path,
              dry_run: bool = False,
              force: bool = False,
              budget_seconds: Optional[int] = None,
              extra_env: Optional[Dict[str, str]] = None,
              runner: Any = subprocess.run) -> CycleResult:
    """دورة واحدة: فحص الاستحقاق → تنفيذ المنفّذ → تسجيل النتيجة."""
    campaign_dir = Path(campaign_dir)
    state_path = Path(state_path)
    res = CycleResult(action="error", campaign="?", started_at=_iso(_now()))
    try:
        campaign = Campaign.load(campaign_dir)
    except CampaignError as e:
        res.errors.append(str(e))
        res.finished_at = _iso(_now())
        return res
    res.campaign = campaign.name
    res.next_due = None

    state = load_state(state_path)
    lr = last_run_at(state)

    if not force and not campaign.is_due(now=_now(), last_run=lr):
        res.action = "skipped_not_due"
        res.reason = (f"آخر تشغيل {_iso(lr) if lr else '—'}؛ "
                      f"الاستحقاق بعد {campaign.pull_interval_hours} ساعة")
        res.finished_at = _iso(_now())
        state.setdefault("history", []).append(res.asdict())
        save_state(state_path, state)
        return res

    env = dict(os.environ)
    if budget_seconds:
        env["FWD_BUDGET"] = str(budget_seconds)
    if extra_env:
        env.update(extra_env)
    res.command = executor_cmd

    if dry_run:
        res.action = "dry_run"
        res.reason = (f"سينفّذ: {executor_cmd} | مصادر نشطة: "
                      f"{len(campaign.active_sources())} | "
                      f"الميزانية: {budget_seconds or 'افتراضية'}ث")
        res.finished_at = _iso(_now())
        state.setdefault("history", []).append(res.asdict())
        save_state(state_path, state)
        return res

    try:
        proc = runner(shlex.split(executor_cmd), env=env, capture_output=True,
                      text=True, timeout=(budget_seconds or 300) + 120)
        res.exit_code = proc.returncode
        res.stdout_tail = (proc.stdout or "")[-2000:]
        res.stderr_tail = (proc.stderr or "")[-2000:]
        res.action = "ran" if proc.returncode == 0 else "error"
        if proc.returncode != 0:
            res.errors.append(f"executor exit={proc.returncode}")
    except FileNotFoundError as e:
        res.errors.append(f"executor not found: {e}")
    except subprocess.TimeoutExpired as e:
        res.errors.append(f"executor timeout after {budget_seconds}s budget")
        res.stdout_tail = (e.stdout or b"").decode()[-1000:] if e.stdout else ""
        res.stderr_tail = (e.stderr or b"").decode()[-1000:] if e.stderr else ""

    res.finished_at = _iso(_now())
    state.setdefault("history", []).append(res.asdict())
    # حدّ أقصى للتاريخ: آخر 200 دورة
    state["history"] = state["history"][-200:]
    save_state(state_path, state)
    return res


# ---------- CLI ----------
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="marathon_suite.runner",
        description="حلقة تشغيل حملات الماراثون — جدولة + تنفيذ منفّذ خارجي + تسجيل")
    ap.add_argument("--campaign", required=True, help="مجلد الحملة (يحوي campaign.yaml)")
    ap.add_argument("--executor", default="", help="أمر المنفّذ (مطلوب للتشغيل الفعلي)")
    ap.add_argument("--state", required=True, help="ملف حالة التشغيل (خارج git)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="تجاهل فحص الاستحقاق")
    ap.add_argument("--status", action="store_true", help="تقرير فقط — بلا تنفيذ")
    ap.add_argument("--budget", type=int, default=None, help="FWD_BUDGET ثانيةً")
    args = ap.parse_args(argv)

    try:
        campaign = Campaign.load(Path(args.campaign))
    except CampaignError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 2

    if args.status:
        print(json.dumps(status(campaign, Path(args.state)), ensure_ascii=False, indent=1))
        return 0

    if not args.executor and not args.dry_run:
        print(json.dumps({"error": "--executor مطلوب للتشغيل الفعلي (أو --dry-run)"},
                         ensure_ascii=False))
        return 2

    res = run_cycle(Path(args.campaign), args.executor, Path(args.state),
                    dry_run=args.dry_run, force=args.force, budget_seconds=args.budget)
    print(json.dumps(res.asdict(), ensure_ascii=False, indent=1))
    return 0 if res.action in ("ran", "dry_run", "skipped_not_due") else 1


if __name__ == "__main__":
    sys.exit(main())
