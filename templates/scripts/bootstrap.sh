#!/usr/bin/env bash
# bootstrap.sh — توليد ملفات Harness لمشروع جديد أو قائم (Harness Engineering v2.0)
#
# ينسخ القوالب ويملأ الحقول {{PROJECT_NAME}} / {{PROJECT_TYPE}}،
# ولا يستبدل أي ملف موجود إلا مع --force=1.
#
# الاستخدام:
#   bash templates/scripts/bootstrap.sh --project=my-new-project \
#        --type=python --target=/path/to/repo --git
#   bash templates/scripts/bootstrap.sh --project=$(basename $PWD) --target=. --force=0
#
# الأنواع (--type): python | fullstack | minimal   (تحدد بوابة init.sh الافتراضية)
# الخروج: 0 نجاح | 1 فشل

set -uo pipefail

TEMPLATE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT=""
TYPE="python"
TARGET="."
GIT_INIT=0
FORCE=0

for arg in "$@"; do
    case "$arg" in
        --project=*) PROJECT="${arg#*=}" ;;
        --type=*)    TYPE="${arg#*=}" ;;
        --target=*)  TARGET="${arg#*=}" ;;
        --git)       GIT_INIT=1 ;;
        --force=*)   FORCE="${arg#*=}" ;;
        --help)
            cat <<EOF
bootstrap.sh — توليد Harness لمشروع
  --project=<اسم>   مطلوب
  --type=<نوع>      python | fullstack | minimal   (افتراضي: python)
  --target=<مسار>   جذر المشروع                  (افتراضي: .)
  --git             init مستودع git إن لم يوجد
  --force=1         استبدال الملفات الموجودة (افتراضي: 0 — يضيف المفقود فقط)
EOF
            exit 0 ;;
        *) echo "معامل غير معروف: $arg" >&2; exit 1 ;;
    esac
done

if [[ -z "$PROJECT" ]]; then
    echo "خطأ: --project مطلوب" >&2
    exit 1
fi

TARGET="$(mkdir -p "$TARGET" && cd "$TARGET" && pwd)"
echo "═══ Harness Bootstrap: $PROJECT ($TYPE) → $TARGET ═══"

if [[ $GIT_INIT -eq 1 && ! -d "$TARGET/.git" ]]; then
    git -C "$TARGET" init -q && echo "✓ git init"
fi

install_file() {
    local src="$1" dst="$2"
    if [[ -f "$dst" && $FORCE -eq 0 ]]; then
        echo "• موجود — تخطي: ${dst#"$TARGET"/}"
        return 0
    fi
    mkdir -p "$(dirname "$dst")"
    sed -e "s/{{PROJECT_NAME}}/$PROJECT/g" -e "s/{{PROJECT_TYPE}}/$TYPE/g" \
        "$src" > "$dst"
    echo "✓ كُتب: ${dst#"$TARGET"/}"
}

install_file "$TEMPLATE_DIR/AGENTS.md"            "$TARGET/AGENTS.md"
install_file "$TEMPLATE_DIR/feature_list.json"    "$TARGET/feature_list.json"
install_file "$TEMPLATE_DIR/progress.md"          "$TARGET/progress.md"
install_file "$TEMPLATE_DIR/session-handoff.md"   "$TARGET/session-handoff.md"
install_file "$TEMPLATE_DIR/gitignore.template"   "$TARGET/.gitignore.harness"
install_file "$TEMPLATE_DIR/env.example"          "$TARGET/.env.example"

# init.sh + الدليل المفهومي من الحزمة المرفقة
if [[ -f "$TEMPLATE_DIR/init.sh.template" ]]; then
    install_file "$TEMPLATE_DIR/init.sh.template" "$TARGET/init.sh"
    chmod +x "$TARGET/init.sh" 2>/dev/null || true
fi
if [[ -f "$TEMPLATE_DIR/HARNESS.md" ]]; then
    install_file "$TEMPLATE_DIR/HARNESS.md" "$TARGET/docs/HARNESS.md"
fi

for s in verify.sh session-handoff.py; do
    if [[ -f "$TEMPLATE_DIR/scripts/$s" ]]; then
        install_file "$TEMPLATE_DIR/scripts/$s" "$TARGET/scripts/$s"
        chmod +x "$TARGET/scripts/$s" 2>/dev/null || true
    fi
done

# التحقق من الصياغة بعد التوليد
if [[ -f "$TARGET/init.sh" ]]; then
    if bash -n "$TARGET/init.sh" 2>/dev/null; then echo "✓ init.sh صياغة سليمة"; else echo "❌ init.sh صياغة مكسورة" >&2; exit 1; fi
fi
if [[ -f "$TARGET/scripts/session-handoff.py" ]]; then
    if python3 -m py_compile "$TARGET/scripts/session-handoff.py" 2>/dev/null; then
        echo "✓ session-handoff.py صياغة سليمة"
    else
        echo "❌ session-handoff.py صياغة مكسورة" >&2
        exit 1
    fi
fi

echo ""
echo "التالي:"
echo "  1) راجع وخصّص $TARGET/AGENTS.md (البوابات + النطاق + الأوامر)"
echo "  2) املأ feature_list.json بالمهام الفعلية"
echo "  3) شغّل: cd $TARGET && ./init.sh"
