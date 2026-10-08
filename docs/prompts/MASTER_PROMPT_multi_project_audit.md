<!-- المصدر: محادثة 1m3ih8eveq98lv7aqc — رسالة 241 -->


# نسخة مُعدَّلة للتنفيذ الذاتي عبر Qwen

## ما يحتاجه Qwen ليقرر بنفسه

البرومبت الأصلي مصمَّم للتفاعل (توقف في كل بوابة). لتشغيله ذاتيًا، أضف **طبقة قرار واضحة** تحدد:

1. **متى يكمل تلقائيًا**
2. **متى يتوقف إجباريًا**  
3. **معايير "نجاح/فشل" كل مرحلة**

---

## البرومبت المُعدَّل — للنسخ إلى Qwen

```
# MASTER PROMPT — Autonomous Multi-Project Integration Audit
# Execution Mode: AUTONOMOUS (with hard safety gates)
# Target: Omni Medical Suite
# Analyst: Qwen acting as Senior Systems Architect

## CORE INSTRUCTION

You are executing a multi-phase audit autonomously. Unlike the 
interactive version, you will proceed through phases WITHOUT 
waiting for user approval — BUT you must STOP IMMEDIATELY at any 
of the HARD GATES listed below.

Between phases, you decide based on the decision rules provided.
Do NOT ask the user for permission between phases.
Do NOT skip phases.
Do NOT proceed past a HARD GATE under any circumstance.

## SAFETY GATES (HARD STOPS)

You MUST stop and report if ANY of these occur:

GATE-1: Repository is not a git worktree
GATE-2: Worktree has uncommitted changes (git status --short non-empty)
GATE-3: Branch is not main or a known feature branch
GATE-4: License conflict detected (AGPL in distributed context, or 
        CC BY-NC in commercial context)
GATE-5: Any subprocess, network egress, or credential access found 
        in upstream code that is not documented
GATE-6: You cannot verify a claim with raw evidence
GATE-7: You are asked to modify OCR runtime code
GATE-8: You detect that you are about to take an action that would 
        modify files outside of docs/audit/

## DECISION RULES (per phase)

After each phase, you decide:

| Outcome | Next Action |
|---------|-------------|
| PROVEN + no risk | Proceed to next phase |
| PARTIALLY PROVEN | Proceed, flag for review |
| UNPROVEN | Proceed, mark as uncertainty |
| CONTRADICTED | HARD STOP, report conflict |
| BLOCKED | HARD STOP, report blocker |
| GATE triggered | HARD STOP immediately |

## PROJECT CLASSIFICATION — ASK ONCE AT START

Before M-00, you must establish:

1. Is omni-medical-suite intended to be commercial? (yes/no/undecided)
2. Will it be distributed externally? (yes/no/internal-only)

Store these. Use them in M-03 (License Audit) to auto-reject projects 
that conflict.

Decision table:
- If commercial=yes AND project has CC BY-NC → AUTO-REJECT project
- If distribution=yes AND project has AGPL → AUTO-REJECT project  
- If commercial=yes AND distribution=yes → only Apache/MIT/BSD allowed

## PHASES

Execute in order: M-00, M-01, M-02, M-03, M-04, M-05, M-06, M-07, M-08.
Report after each phase in the specified format.
Do NOT skip phases based on expected outcome.
Do NOT combine phases.

### Phase details:

M-00: Pre-flight verification
  Commands to run:
    git -C /home/z/my-project/repos/omni-medical-suite rev-parse --is-inside-work-tree
    git -C ... status --short
    git -C ... branch --show-current
    git -C ... remote -v
  Output format:
    Repository, Branch, HEAD, Worktree, Remote
    Status: OK | BLOCKED
  Decision: If OK → proceed to M-01. If BLOCKED → HARD STOP.

M-01: For each of 4 projects, create technical card with:
  - Repository URL, License (from LICENSE file only), Latest SHA
  - Runtime requirements
  - Core concepts / features
  - Integration points
  Evidence: raw git ls-remote output
  Decision: proceed to M-02 for all projects that pass license pre-check
  
M-02: Forensic source audit
  Clone each project to /tmp/audit/<project-name> (read-only)
  Search for: subprocess, exec, network calls, credential access
  Evidence: exact grep commands + line numbers
  Decision: if any project has undocumented network egress or 
           credential access → flag but proceed to M-03
  
M-03: License audit (CRITICAL)
  For each project, produce decision:
    ALLOWED | BLOCKED | CONDITIONAL
  Rules based on project_classification from start
  Evidence: LICENSE file content (first 20 lines)
  Decision: BLOCKED projects are excluded from subsequent phases
  
M-04: Component mapping
  For each non-BLOCKED project, determine:
    ADOPT | ADAPT | WRAP | PILOT | STUDY_ONLY | DEFER | REJECT
  Evidence: table with capability, need, risk, action
  
M-05: Security audit
  Run credential scans, egress scans
  Decision: if critical finding → HARD STOP
  
M-06: Pilot (only if license + security pass)
  Skip if resources unavailable
  Decision: document why skipped or run locally
  
M-07: Decision matrix
  For each capability: final action
  
M-08: Final package
  Write to docs/audit/MULTI_PROJECT_INTEGRATION_PACKAGE.md
  
## REPORTING FORMAT (after each phase)

=== PHASE M-XX — <NAME> ===

Status: PROVEN | PARTIALLY_PROVEN | UNPROVEN | CONTRADICTED | BLOCKED | NOT_EXECUTED

Files inspected:
  - <path1>
  - <path2>

Commands executed:
  $ <cmd1>
  $ <cmd2>

Raw evidence:
  <output excerpt>

Findings:
  1. <finding> [Status]
  2. <finding> [Status]

Risks remaining:
  - <risk>

Next phase: M-YY
Reason for proceeding / stopping: <one sentence>

=== END PHASE M-XX ===

## ABSOLUTE PROHIBITIONS

- ❌ Do not modify any file outside docs/audit/
- ❌ Do not run pip install, npm install, cargo install, apt install
- ❌ Do not download models
- ❌ Do not call external APIs (except git ls-remote for license check)
- ❌ Do not commit, push, or create branches
- ❌ Do not write to files in packages/, src/, app/, or any code dir
- ❌ Do not proceed past any HARD GATE
- ❌ Do not skip evidence for any claim
- ❌ Do not assume user answers to project_classification questions

## BEGIN

Start with the project_classification questions. If you cannot 
determine the answers from context, use UNDECIDED for both and 
mark License Audit (M-03) as requiring human review.

Then execute M-00.

Then decide whether to proceed to M-01 based on the decision rules.

Continue autonomously until you either:
(a) reach M-08 and complete the final package
(b) trigger a HARD GATE and stop
(c) run out of tool calls or resources

Report after each phase. Do not wait for user approval between phases.
```

---

## ما سيفعله Qwen فعليًا

| المرحلة | القدرة | القيود |
|---------|-------|--------|
| M-00 (فحص المستودع) | ✅ إذا كان لديه وصول لجهازك | ❌ إن كان مجرد chat |
| M-01 (بطاقات تقنية) | ✅ يستطيع البحث على GitHub | قد لا يصل لـ `git ls-remote` |
| M-02 (تدقيق الكود) | ⚠️ يستطيع التحليل إن استنسخ | يحتاج وصول شبكة |
| M-03 (الترخيص) | ✅ من LICENSE على GitHub | دقيق |
| M-04 إلى M-08 | ✅ تحليل معماري | لا يحتاج تنفيذ |

**القيد الأساسي**: إذا كان Qwen **chat فقط** (بلا tool access)، سيصل إلى **M-04 كأقصى حد** — لا يستطيع تشغيل `git` أو قراءة ملفات محلية.

**إن كان Qwen Code / Qwen-Agent**: يستطيع تنفيذ كل المراحل.

---

## قبل أن تُرسل

**تحقق من قدرات Qwen في بيئتك**:

1. هل يستطيع تشغيل أوامر terminal؟ (نعم/لا)
2. هل يستطيع قراءة ملفات من جهازك؟ (نعم/لا)
3. هل يستطيع الوصول للإنترنت؟ (نعم/لا)

**إن كانت الإجابات كلها "لا"** → أرسل له فقط:
- روابط GitHub الأربعة
- الأسئلة الحرجة (تجاري؟ موزَّع؟)
- سيُنتج تحليلًا نصيًا **بدون** تدقيق كود

**إن كانت "نعم"** → أرسل البرومبت المُعدَّل أعلاه.

---

## سؤال واحد

**ما نسخة Qwen التي تستخدمها؟**

- `Qwen Chat` (الويب العادي) ← chat فقط، بلا تنفيذ
- `Qwen Code` ← لديه terminal
- `Qwen-Agent` / MCP-enabled ← لديه ملفات + terminal
- عبر API (بدون واجهة) ← يعتمد على ما تعطيه

**أخبرني بالضبط، وسأُعدّل البرومبت لقدراته الفعلية.**
