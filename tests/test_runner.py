# tests/test_runner.py — اختبارات حلقة التشغيل (بلا شبكة، بلا تيليجرام)
"""منفّذ وهمي (echo/python -c) بدل tg_forward_ortho — يختبر الجدولة والتسجيل
والصدق: التخطي لا يُحدّث آخر تشغيل، والتنفيذ يُسجَّل بنتيجته."""
import json
import sys
from pathlib import Path

import pytest

from marathon_suite.campaign import Campaign, CampaignError
from marathon_suite.runner import load_state, run_cycle, status

REPO_ROOT = Path(__file__).resolve().parents[1]
ORTHO_DIR = REPO_ROOT / "campaigns" / "ortho"


_FAKE_SEQ = {"n": 0}


def _fake_executor(tmp_path: Path, code: str) -> str:
    """سكربت وهمي يخرج بنجاح/فشل حسب الكود المعطى — ملف مميز لكل منفّذ."""
    _FAKE_SEQ["n"] += 1
    p = tmp_path / f"fake_executor_{_FAKE_SEQ['n']}.py"
    p.write_text(code, encoding="utf-8")
    return f"{sys.executable} {p}"


# ---------- 1. التخطي والاستحقاق ----------
def test_first_run_is_due(tmp_path: Path):
    st = tmp_path / "state.json"
    s = status(Campaign.load(ORTHO_DIR), st)
    assert s["is_due"] is True
    assert s["next_due"] == "now (لم يُشغَّل بعد)"


def test_skipped_not_due_after_recent_run(tmp_path: Path):
    st = tmp_path / "state.json"
    cmd = _fake_executor(tmp_path, "print('ok')")
    r1 = run_cycle(ORTHO_DIR, cmd, st, force=True)
    assert r1.action == "ran" and r1.exit_code == 0
    # دورة ثانية مباشرة → تخطٍ (لا مرّت 6 ساعات)
    r2 = run_cycle(ORTHO_DIR, cmd, st)
    assert r2.action == "skipped_not_due"
    # التخطي سُجّل في التاريخ لكنه لا يصبح last_run
    state = load_state(st)
    assert len(state["history"]) == 2
    assert state["history"][-1]["action"] == "skipped_not_due"


# ---------- 2. التنفيذ الفعلي والتسجيل ----------
def test_run_records_result_and_failures(tmp_path: Path):
    st = tmp_path / "state.json"
    ok = _fake_executor(tmp_path, "print('forwarded 3')")
    bad = _fake_executor(tmp_path, "import sys; sys.exit(3)")
    r1 = run_cycle(ORTHO_DIR, ok, st, force=True)
    assert r1.action == "ran" and "forwarded 3" in r1.stdout_tail
    r2 = run_cycle(ORTHO_DIR, bad, st, force=True)
    assert r2.action == "error" and r2.exit_code == 3 and r2.errors
    # الفشل لا يصبح last_run — نحذف النجاح من التاريخ: ما تبقى فشل فقط
    state = load_state(st)
    state["history"] = [h for h in state["history"] if h["action"] != "ran"]
    (st).write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    r3 = run_cycle(ORTHO_DIR, ok, st)   # بلا force: لا last_run ناجح → مستحقة
    assert r3.action == "ran"           # الفشل لا يجمد الجدولة


def test_budget_env_passed_to_executor(tmp_path: Path):
    st = tmp_path / "state.json"
    p = tmp_path / "show_env.py"
    p.write_text("import os; print('BUDGET=' + os.environ.get('FWD_BUDGET', ''))",
                 encoding="utf-8")
    r = run_cycle(ORTHO_DIR, f"{sys.executable} {p}", st, force=True, budget_seconds=77)
    assert "BUDGET=77" in r.stdout_tail


def test_history_capped_at_200(tmp_path: Path):
    st = tmp_path / "state.json"
    cmd = _fake_executor(tmp_path, "print('x')")
    for _ in range(205):
        run_cycle(ORTHO_DIR, cmd, st, force=True)
    assert len(load_state(st)["history"]) == 200


# ---------- 3. العدسة الصادقة ----------
def test_dry_run_executes_nothing_but_records(tmp_path: Path):
    st = tmp_path / "state.json"
    r = run_cycle(ORTHO_DIR, "echo should-not-run", st, dry_run=True, force=True)
    assert r.action == "dry_run"
    assert len(load_state(st)["history"]) == 1


def test_missing_executor_command_is_error(tmp_path: Path):
    st = tmp_path / "state.json"
    r = run_cycle(ORTHO_DIR, "/nonexistent/executor-xyz", st, force=True)
    assert r.action == "error" and any("not found" in e for e in r.errors)


def test_broken_campaign_rejected(tmp_path: Path):
    empty = tmp_path / "nope"
    empty.mkdir()
    r = run_cycle(empty, "echo hi", tmp_path / "state.json", force=True)
    assert r.action == "error" and r.errors  # CampaignError → نتيجة خطأ صريحة
