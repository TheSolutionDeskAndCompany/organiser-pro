# Step 4 — Automate per-repo upgrades

# We'll start with one repo (OrganiserPro). This script:
# - clones the repo
# - creates a branch
# - adds any missing standard files (README, LICENSE, workflows, etc)
# - pushes and opens a PR automatically

# Save this as standardize-one.sh in your Codespace.

#!/usr/bin/env bash
set -euo pipefail

OWNER="${OWNER:-TheSolutionDeskAndCompany}"
REPO="${1:-organiser-pro}"   # pass repo name as arg, default organiser-pro
BRANCH="chore/standardize-repo"
WORKDIR="$(pwd)"
TMPSTD="$WORKDIR/_std"

need() { command -v "$1" >/dev/null || { echo "Missing $1"; exit 1; }; }
need gh; need git; need jq

# Build standards directory (files are only copied if missing)
rm -rf "$TMPSTD"; mkdir -p "$TMPSTD/.github/workflows" "$TMPSTD/.github/ISSUE_TEMPLATE"

# README skeleton (only used if the repo has none)
cat > "$TMPSTD/README.md" <<'MD'
# <Project Name> · <one-line hook>

[![CI](./actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)
[![Release](./actions/workflows/release-please.yml/badge.svg)](../../actions/workflows/release-please.yml)
[![CodeQL](./actions/workflows/codeql.yml/badge.svg)](../../actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Short elevator pitch: who it’s for, the outcome it creates, and why it’s different.

## ✨ Features
- ...

## 📦 Installation
```bash
# npm i <pkg>   |   pip install <pkg>
```

## 🚀 Quick Start
```bash
# minimal example
```

## 🧪 Tests
```bash
npm test | pytest -q
```

## 🛠 Configuration
Describe env vars / config.

## 🤝 Contributing
See CONTRIBUTING.md and CODE_OF_CONDUCT.md.

## 🛡 Security
See SECURITY.md.

## 💬 Support
See SUPPORT.md.

## 🧾 License
MIT © The Solution Desk
MD

# MIT license (only copied if missing)
cat > "$TMPSTD/LICENSE" <<'LIC'
MIT License

Copyright (c) 2025 The Solution Desk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
[...]
LIC

# CI workflow (Node + Python; no-ops if project files absent)
cat > "$TMPSTD/.github/workflows/ci.yml" <<'YML'
name: CI
on:
  push: { branches: [main, master] }
  pull_request:
jobs:
  build-test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { language: [node, python] }
    steps:
      - uses: actions/checkout@v4

      - name: Node setup
        if: matrix.language == 'node'
        uses: actions/setup-node@v4
        with: { node-version: 'lts/*', cache: 'npm' }
      - if: matrix.language == 'node'
        run: |
          if [ -f package.json ]; then
            npm ci
            npm run build --if-present
            npm test --if-present
          fi

      - name: Python setup
        if: matrix.language == 'python'
        uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - if: matrix.language == 'python'
        run: |
          if [ -f pyproject.toml ] || [ -f requirements.txt ]; then
            python -m pip install -U pip
            [ -f requirements.txt ] && pip install -r requirements.txt || true
            [ -f pyproject.toml ] && pip install -e . || true
            if command -v pytest >/dev/null 2>&1; then pytest -q || true; fi
          fi
YML

# Dependabot
cat > "$TMPSTD/.github/dependabot.yml" <<'YML'
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule: { interval: weekly }
  - package-ecosystem: pip
    directory: "/"
    schedule: { interval: weekly }
  - package-ecosystem: github-actions
    directory: "/"
    schedule: { interval: monthly }
YML

# CodeQL
cat > "$TMPSTD/.github/workflows/codeql.yml" <<'YML'
name: CodeQL
on:
  push: { branches: [main, master] }
  pull_request:
  schedule: [{ cron: '0 6 * * 1' }]
jobs:
  analyze:
    uses: github/codeql-action/.github/workflows/codeql.yml@v3
    with: { languages: 'javascript,python' }
YML

# Repo docs (only if missing locally — org-level defaults already cover public repos)
cat > "$TMPSTD/CODE_OF_CONDUCT.md" <<'MD'
# Code of Conduct
This project follows the Contributor Covenant v2.1.
MD

cat > "$TMPSTD/CONTRIBUTING.md" <<'MD'
# Contributing
- Branching: feat/*, fix/*, chore/*
- Conventional commits recommended
- Lint & test before PR
MD

cat > "$TMPSTD/SECURITY.md" <<'MD'
# Security
Report vulnerabilities to security@thesolutiondesk.ca (72h acknowledgement).
MD

cat > "$TMPSTD/SUPPORT.md" <<'MD'
# Support
Open an Issue. For Q&A, use Discussions if enabled.
MD

cat > "$TMPSTD/.github/ISSUE_TEMPLATE/repo_audit.yml" <<'YML'
name: 🔎 Repo Audit
description: Review this repository against standards
labels: ["audit","good first issue"]
body:
  - type: checkboxes
    id: basics
    attributes:
      label: Basics
      options:
        - label: Name & description clear
        - label: Topics set
        - label: LICENSE present
  - type: checkboxes
    id: docs
    attributes:
      label: Docs
      options:
        - label: README template
        - label: CONTRIBUTING
        - label: CODE_OF_CONDUCT
        - label: SECURITY
        - label: SUPPORT
  - type: checkboxes
    id: auto
    attributes:
      label: Automation
      options:
        - label: CI green
        - label: Release-Please enabled
        - label: Dependabot enabled
        - label: CodeQL enabled
YML

cat > "$TMPSTD/.github/pull_request_template.md" <<'MD'
## Summary
## Changes
- [ ] ...
## Checklist
- [ ] Tests pass
- [ ] Docs updated
MD

# Clone repo
[ -d "$REPO" ] || gh repo clone "$OWNER/$REPO" "$REPO"
cd "$REPO"

# Figure default branch
DEFAULT_BRANCH="$(gh repo view "$OWNER/$REPO" --json defaultBranchRef -q .defaultBranchRef.name)"
git fetch origin
git checkout -B "$BRANCH" "$DEFAULT_BRANCH"

# Helper: copy only if missing
copy_if_missing() { local s="$1"; local d="$2"; [ -e "$d" ] || { mkdir -p "$(dirname "$d")"; cp "$s" "$d"; echo "  + Added $(basename "$d")"; }; }

copy_if_missing "$TMPSTD/README.md" "README.md"
copy_if_missing "$TMPSTD/LICENSE" "LICENSE"
copy_if_missing "$TMPSTD/.github/workflows/ci.yml" ".github/workflows/ci.yml"
copy_if_missing "$TMPSTD/.github/workflows/codeql.yml" ".github/workflows/codeql.yml"
copy_if_missing "$TMPSTD/.github/dependabot.yml" ".github/dependabot.yml"
copy_if_missing "$TMPSTD/CODE_OF_CONDUCT.md" "CODE_OF_CONDUCT.md"
copy_if_missing "$TMPSTD/CONTRIBUTING.md" "CONTRIBUTING.md"
copy_if_missing "$TMPSTD/SECURITY.md" "SECURITY.md"
copy_if_missing "$TMPSTD/SUPPORT.md" "SUPPORT.md"
copy_if_missing "$TMPSTD/.github/ISSUE_TEMPLATE/repo_audit.yml" ".github/ISSUE_TEMPLATE/repo_audit.yml"
copy_if_missing "$TMPSTD/.github/pull_request_template.md" ".github/pull_request_template.md"

# Release-Please workflow depends on project type
RELTYPE="simple"
[ -f package.json ] && RELTYPE="node"
[ -f pyproject.toml ] && RELTYPE="python"
mkdir -p ".github/workflows"
cat > ".github/workflows/release-please.yml" <<YML
name: Release Please
on:
  push: { branches: [$DEFAULT_BRANCH] }
permissions: { contents: write, pull-requests: write }
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/release-please-action@v4
        with:
          release-type: $RELTYPE
          package-name: $REPO
YML

# Commit if anything changed
if git status --porcelain | grep .; then
  git add .
  git commit -m "chore(standard): add repo standard files (README, CI, CodeQL, Dependabot, docs)"
  git push -u origin "$BRANCH" --force-with-lease
  gh pr create --title "chore(standard): align with The Solution Desk repo standards" \
               --body "Adds standard workflows, docs, and templates. Non-destructive: existing files preserved." \
               --label "chore" || echo "(PR may already exist)"
else
  echo "No changes needed."
fi
