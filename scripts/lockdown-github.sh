#!/usr/bin/env bash
# Lock down jasonet/deep-claude for solo maintenance.
# Keeps stars and forks enabled; disables external contribution surfaces.
#
# Prerequisite: gh auth login -h github.com (must have admin scope on the repo).
#
# Re-run every 6 months to renew interaction limits (GitHub API caps the
# expiry at six_months for collaborators_only mode).

set -euo pipefail

OWNER="jasonet"
REPO="deep-claude"
SLUG="${OWNER}/${REPO}"

echo "==> Locking down ${SLUG}"

if ! gh auth status >/dev/null 2>&1; then
    echo "[error] gh is not authenticated. Run: gh auth login -h github.com" >&2
    exit 1
fi

echo "[1/4] Disabling Issues, Wiki, Projects, Discussions"
gh api -X PATCH "repos/${SLUG}" \
    -F has_issues=false \
    -F has_wiki=false \
    -F has_projects=false \
    -F has_discussions=false \
    --silent

echo "[2/4] Forks/stars rely on public-repo defaults (no API call needed)"

echo "[3/4] Limiting interactions to collaborators only (expires in 6 months)"
gh api -X PUT "repos/${SLUG}/interaction-limits" \
    -f limit=collaborators_only \
    -f expiry=six_months \
    --silent

echo "[4/4] Protecting main: PRs require code-owner review"
gh api -X PUT "repos/${SLUG}/branches/main/protection" \
    --input - >/dev/null <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

echo
echo "Done. Verify in browser:"
echo "  https://github.com/${SLUG}/settings"
echo "  https://github.com/${SLUG}/settings/branches"
echo "  https://github.com/${SLUG}/settings/interaction_limits"
