# Setting up GitHub Mirror for enrichlayer-py

This guide explains how to set up GitHub as a mirror of your GitLab repository, allowing GitHub to serve as a public-facing repository for community issues while keeping GitLab as your primary development repository.

## Overview

- **GitLab**: Primary repository (source of truth) for development, CI/CD, and merge requests
- **GitHub**: Public mirror for visibility, issue tracking, and community engagement

## Step 1: Create GitHub Repository

1. Create a new repository on GitHub:
   - Go to https://github.com/new
   - Name: `enrichlayer-py` (or `enrichlayer-python`)
   - Description: "Python client library for EnrichLayer API - Alternative to Proxycurl API with compatible interface"
   - Public repository
   - **DO NOT** initialize with README, .gitignore, or license (we'll push from GitLab)

2. Note the GitHub repository URL:
   ```
   https://github.com/enrichlayer/enrichlayer-py.git
   ```

## Step 2: Configure GitLab Repository Mirroring

### Option A: Push Mirroring (Recommended)

1. In your GitLab project, go to:
   **Settings → Repository → Mirroring repositories**

2. Add push mirror:
   - Git repository URL: `https://github.com/enrichlayer/enrichlayer-py.git`
   - Mirror direction: Push
   - Authentication method: Password
   - Password: Use a GitHub Personal Access Token (PAT) with `repo` scope
     - Create at: https://github.com/settings/tokens/new
     - Scopes needed: `repo` (all)
   - Keep divergent refs: Unchecked (recommended)
   - Mirror only protected branches: Optional (if you only want to mirror main/master)

3. Click "Mirror repository"

4. Test by clicking "Update now" button

### Option B: Using GitLab CI/CD (Alternative)

Add to `.gitlab-ci.yml`:

```yaml
mirror-to-github:
  stage: deploy
  image: alpine/git:latest
  script:
    - git remote add github https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/enrichlayer/enrichlayer-py.git
    - git push github HEAD:main --force
  only:
    - main
  variables:
    GIT_STRATEGY: clone
    GIT_DEPTH: 0
```

Set CI/CD variables in GitLab:
- `GITHUB_USERNAME`: Your GitHub username
- `GITHUB_TOKEN`: GitHub Personal Access Token

## Step 3: Configure GitHub Repository

### Add Repository Description and Topics

1. Go to GitHub repository settings (⚙️ icon)
2. Add topics: `python`, `enrichlayer`, `proxycurl`, `api-client`, `linkedin`, `data-enrichment`
3. Add website: `https://enrichlayer.com`

### Set Up Branch Protection

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - Require pull request reviews before merging: ❌ (since we're mirroring)
   - Restrict who can push to matching branches: ✅
   - Add yourself/bot as exception

### Disable Unnecessary Features

Since this is a mirror:
1. Settings → General → Features:
   - Wikis: ❌
   - Projects: ❌ (optional)
   - Discussions: ❌ (use Issues instead)

2. Settings → General → Pull Requests:
   - Automatically delete head branches: ✅

## Step 4: Add GitHub-Specific Files

These files should be added to inform users about the mirroring setup:

### Create `.github/README_GITHUB.md`:

```markdown
# ⚠️ This is a Mirror Repository

This repository is a **read-only mirror** of our primary repository hosted on GitLab.

## 🏠 Primary Repository
**Development happens on GitLab**: [gitlab.com/enrichlayer/enrichlayer-py](https://gitlab.com/enrichlayer/enrichlayer-py)

## 🐛 Reporting Issues
✅ **Please report issues HERE on GitHub** - we actively monitor GitHub issues!

## 🔧 Contributing Code
❌ **Pull Requests on GitHub will be closed**
✅ **Please submit Merge Requests on GitLab**: [GitLab MR Guide](https://gitlab.com/enrichlayer/enrichlayer-py/-/merge_requests)

## 📦 Installation
The package is available on PyPI:
```bash
pip install enrichlayer-api[gevent]
```

## Why This Setup?
- GitHub provides better visibility and issue tracking for the community
- GitLab provides better CI/CD and development workflows for maintainers
- This is a common pattern used by many projects

Thank you for your understanding! 🙏
```

### Update Main README.md

Add badges at the top:

```markdown
[![PyPI version](https://badge.fury.io/py/enrichlayer-api.svg)](https://pypi.org/project/enrichlayer-api/)
[![GitLab Repository](https://img.shields.io/badge/GitLab-Repository-orange?logo=gitlab)](https://gitlab.com/enrichlayer/enrichlayer-py)
[![GitHub Mirror](https://img.shields.io/badge/GitHub-Mirror-black?logo=github)](https://github.com/enrichlayer/enrichlayer-py)
[![Report Issues](https://img.shields.io/badge/Issues-GitHub-green?logo=github)](https://github.com/enrichlayer/enrichlayer-py/issues)
```

## Step 5: Handle Pull Requests

Since people might still try to open PRs on GitHub:

### Create `.github/pull_request_template.md`:

```markdown
## ⚠️ This is a Mirror Repository

Thank you for your contribution! However, this GitHub repository is a read-only mirror.

**Please submit your changes as a Merge Request on our GitLab repository:**
🔗 https://gitlab.com/enrichlayer/enrichlayer-py/-/merge_requests/new

### Why?
- Our development workflow and CI/CD are set up on GitLab
- This GitHub repository is automatically synced from GitLab

### Steps:
1. Close this Pull Request
2. Fork our GitLab repository
3. Submit your changes as a Merge Request on GitLab
4. Our team will review it there

We apologize for the inconvenience and appreciate your understanding! 🙏

---
*This PR will be automatically closed.*
```

### GitHub Action to Auto-Close PRs

Create `.github/workflows/close-prs.yml`:

```yaml
name: Close Pull Requests

on:
  pull_request:
    types: [opened, reopened]

jobs:
  close:
    runs-on: ubuntu-latest
    steps:
      - uses: peter-evans/close-pull@v3
        with:
          comment: |
            Thank you for your contribution! ❤️
            
            This GitHub repository is a **read-only mirror**. Please submit your changes on GitLab:
            
            🔗 **[Create Merge Request on GitLab](https://gitlab.com/enrichlayer/enrichlayer-py/-/merge_requests/new)**
            
            For more information, see our [Contributing Guide](https://gitlab.com/enrichlayer/enrichlayer-py/-/blob/main/CONTRIBUTING.md).
```

## Step 6: Issue Management

GitHub Issues will be your primary community interaction point.

### Enable Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```yaml
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Code snippet or command
2. Expected behavior
3. Actual behavior

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.9]
- Package version: [e.g. enrichlayer-api==0.1.0]
- Async library: [gevent/asyncio/twisted]

**Additional context**
Add any other context about the problem here.
```

Create `.github/ISSUE_TEMPLATE/feature_request.md`:

```yaml
---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

Create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: true
contact_links:
  - name: GitLab Repository (Development)
    url: https://gitlab.com/enrichlayer/enrichlayer-py
    about: For contributing code, please use our GitLab repository
  - name: Documentation
    url: https://docs.enrichlayer.com
    about: Check our documentation for usage examples
  - name: EnrichLayer Support
    url: mailto:support@enrichlayer.com
    about: For account or API key issues
```

## Step 7: Sync Monitoring

### GitHub Action to Check Sync Status

Create `.github/workflows/sync-monitor.yml`:

```yaml
name: Monitor GitLab Sync

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  check-sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: Add GitLab remote
        run: |
          git remote add gitlab https://gitlab.com/enrichlayer/enrichlayer-py.git
          git fetch gitlab
          
      - name: Check if in sync
        run: |
          LOCAL=$(git rev-parse HEAD)
          REMOTE=$(git rev-parse gitlab/main)
          if [ "$LOCAL" != "$REMOTE" ]; then
            echo "⚠️ GitHub mirror is out of sync with GitLab!"
            echo "Local: $LOCAL"
            echo "Remote: $REMOTE"
            exit 1
          else
            echo "✅ GitHub mirror is in sync with GitLab"
          fi
```

## Step 8: Community Files

### Create `.github/CONTRIBUTING.md`:

```markdown
# Contributing to enrichlayer-py

Thank you for your interest in contributing! 🎉

## 🏠 Development Repository

**All development happens on GitLab**: [gitlab.com/enrichlayer/enrichlayer-py](https://gitlab.com/enrichlayer/enrichlayer-py)

This GitHub repository is a **read-only mirror** used for:
- 🐛 Issue tracking and community discussions
- 📦 Package discovery
- 📚 Documentation viewing

## 🐛 Reporting Issues

✅ **Please report issues here on GitHub!** We actively monitor and respond to GitHub issues.

## 🔧 Contributing Code

To contribute code:

1. **Fork the GitLab repository** (not this GitHub mirror)
2. Create a feature branch
3. Make your changes
4. Submit a **Merge Request on GitLab**

Detailed steps:
```bash
# Clone your GitLab fork
git clone https://gitlab.com/YOUR_USERNAME/enrichlayer-py.git
cd enrichlayer-py

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add your feature"

# Push to your fork
git push origin feature/your-feature-name
```

Then create a Merge Request on GitLab.

## 📋 Development Setup

See our [Development Guide](https://gitlab.com/enrichlayer/enrichlayer-py/-/blob/main/DEVELOPMENT.md) on GitLab.

## ❓ Questions?

- For bugs and features: Open an issue here on GitHub
- For development questions: Use GitLab discussions
- For support: support@enrichlayer.com
```

## Maintenance Notes

1. **Mirror Updates**: GitLab will automatically push to GitHub based on your mirror settings
2. **Issue Triage**: Regularly check GitHub issues and transfer actionable items to GitLab
3. **Community Engagement**: Respond to GitHub issues promptly
4. **Documentation**: Keep README and community files updated on both platforms

## Troubleshooting

### Mirror Not Updating
1. Check GitLab mirror settings for errors
2. Verify GitHub PAT hasn't expired
3. Check branch protection rules on GitHub
4. Use "Update now" button in GitLab mirror settings

### Authentication Issues
1. Regenerate GitHub Personal Access Token
2. Ensure token has `repo` scope
3. Update token in GitLab mirror settings

### Diverged Repositories
1. This shouldn't happen with push mirroring
2. If it does, force push from GitLab:
   ```bash
   git push --mirror https://github.com/enrichlayer/enrichlayer-py.git
   ```