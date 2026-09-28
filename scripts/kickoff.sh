#!/usr/bin/env bash
#
# Initialize the hackathon project repository at official kickoff.
#
# This folder is the hackathon project folder. It is deliberately NOT a git
# repository before the official start of the event, so that the submission
# history begins at kickoff and contains no prior work.
#
# This script performs the kickoff. It initializes the repository and sets the
# default branch, but it does NOT create a commit unless you explicitly pass
# --commit. That default is deliberate: a commit made before the official
# start would contaminate the submission history.
#
# Usage:
#   scripts/kickoff.sh [--commit] [--only-product] [-m "message"]
#
# Examples:
#   scripts/kickoff.sh
#   scripts/kickoff.sh --commit -m "chore: initialize project workspace"
#   scripts/kickoff.sh --commit --only-product -m "feat: initial structure"

set -euo pipefail

COMMIT=0
ONLY_PRODUCT=0
MESSAGE="chore: initialize project workspace"

while [ $# -gt 0 ]; do
    case "$1" in
        --commit)       COMMIT=1; shift ;;
        --only-product) ONLY_PRODUCT=1; shift ;;
        -m|--message)   MESSAGE="${2:?--message needs a value}"; shift 2 ;;
        -h|--help)      sed -n '2,25p' "$0"; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# --- Refuse to clobber an existing repository -----------------------------
if [ -e ".git" ]; then
    echo "A .git directory already exists in $PROJECT_ROOT." >&2
    echo "This script is for kickoff only. Use normal git commands." >&2
    exit 1
fi

echo "Project root: $PROJECT_ROOT"
echo

# --- Initialize the repository --------------------------------------------
git init -q
git symbolic-ref HEAD refs/heads/main
echo "Initialized git repository on branch 'main'."

# --- Report what is present ------------------------------------------------
TOOLKIT_RE='^\.agents/|^AGENTS\.md$|^HANDOFF\.md$|^docs/|^scripts/|^\.gitignore$|^\.gitattributes$|^\.env\.example$'

ALL="$(git ls-files --others --exclude-standard)"
ALL_COUNT="$(printf '%s\n' "$ALL" | grep -c . || true)"
PRODUCT="$(printf '%s\n' "$ALL" | grep -Ev "$TOOLKIT_RE" | grep -c . || true)"

echo
echo "Files detected: $ALL_COUNT total" 
echo "  product paths : $PRODUCT"
echo "  toolkit paths : $((ALL_COUNT - PRODUCT))"

if [ "$ONLY_PRODUCT" -eq 1 ]; then
    if [ "$PRODUCT" -eq 0 ]; then
        echo "--only-product was requested but no product paths were found." >&2
        exit 1
    fi
    printf '%s\n' "$ALL" | grep -Ev "$TOOLKIT_RE" | while IFS= read -r f; do
        git add -- "$f"
    done
    echo
    echo "Staged product paths only:"
    printf '%s\n' "$ALL" | grep -Ev "$TOOLKIT_RE" | sed 's/^/  /'
else
    git add -A
    echo
    echo "Staged everything (--only-product not used)."
fi

# --- Commit only when explicitly asked -------------------------------------
if [ "$COMMIT" -eq 0 ]; then
    echo
    echo "NO COMMIT CREATED." 
    echo "That is the safe default. Review the staged list, then run:"
    echo "  scripts/kickoff.sh --commit -m \"$MESSAGE\""
    echo
    echo "Only commit once the official hackathon has started."
    exit 0
fi

COUNT="$(git rev-list --all --count 2>/dev/null || echo 0)"
if [ "$COUNT" -ne 0 ]; then
    echo "Expected an empty history, found $COUNT commits. Aborting." >&2
    exit 1
fi

git commit -q -m "$MESSAGE"
echo
echo "Created first commit: $(git rev-parse --short HEAD)  $MESSAGE"
echo
echo "History now begins at the official start of the event."
