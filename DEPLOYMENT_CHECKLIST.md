# Deployment Checklist

Use this checklist before deploying your Pulseway MCP Server to GitHub.

## Pre-Deployment Checklist

### 1. Code Review
- [ ] All code is properly formatted and linted
- [ ] No hardcoded credentials or secrets in code
- [ ] All functions have docstrings
- [ ] Type hints are used consistently
- [ ] Error handling is in place

### 2. Documentation
- [ ] README.md is complete and accurate
- [ ] QUICKSTART.md has correct installation steps
- [ ] API endpoints are documented
- [ ] Usage examples are provided
- [ ] Troubleshooting section is helpful

### 3. Security
- [ ] `secrets.env` is NOT committed (check `.gitignore`)
- [ ] `secrets.env.example` has no real credentials
- [ ] No API keys or passwords in any files
- [ ] File permissions are appropriate
- [ ] Security best practices are documented

### 4. Testing
- [ ] All unit tests pass: `uv run pytest`
- [ ] Test coverage is adequate
- [ ] Edge cases are covered
- [ ] Mock API responses work correctly
- [ ] Error cases are tested

### 5. Configuration Files
- [ ] `pyproject.toml` has correct dependencies
- [ ] `pyproject.toml` has correct version number
- [ ] `.gitignore` includes all sensitive files
- [ ] `.github/workflows/ci.yml` is configured
- [ ] LICENSE file is present (MIT)

### 6. Repository Setup
- [ ] Repository name is correct
- [ ] Repository description is clear
- [ ] Topics/tags are added (mcp, claude, pulseway, api)
- [ ] README is set as default
- [ ] Branch protection rules (optional but recommended)

## GitHub Setup Steps

### 1. Create Repository on GitHub
```bash
# On GitHub.com:
# 1. Click "New Repository"
# 2. Name: pulseway-mcp-server
# 3. Description: MCP server for Pulseway PSA API integration with Claude AI
# 4. Public or Private (your choice)
# 5. Do NOT initialize with README (we have one)
# 6. Click "Create Repository"
```

### 2. Initial Commit and Push
```bash
cd pulseway-mcp-server

# Initialize git (if not already done)
git init

# Add all files
git add .

# Verify no secrets are staged
git status
# Make sure secrets.env is NOT listed!

# Commit
git commit -m "Initial commit: Pulseway MCP Server v0.1.0

- Implement MCP server for Pulseway PSA API
- Add support for tickets, invoices, opportunities, accounts, and time logs
- Include comprehensive documentation and examples
- Add unit tests and GitHub Actions CI/CD
- Configure security best practices"

# Add remote
git remote add origin https://github.com/yourusername/pulseway-mcp-server.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Configure GitHub Repository Settings

#### Repository Settings
- [ ] Add description: "MCP server for Pulseway PSA API integration with Claude AI"
- [ ] Add website: Link to Pulseway or your docs
- [ ] Add topics: `mcp`, `claude`, `pulseway`, `psa`, `api`, `python`, `async`

#### About Section
- [ ] Edit repository details
- [ ] Add relevant tags
- [ ] Include homepage URL if applicable

#### Actions
- [ ] Enable GitHub Actions
- [ ] Verify CI workflow runs successfully
- [ ] Check workflow permissions

#### Security
- [ ] Enable Dependabot alerts (recommended)
- [ ] Enable Dependabot security updates (recommended)
- [ ] Add SECURITY.md if needed

### 4. Create First Release

```bash
# Tag the release
git tag -a v0.1.0 -m "Initial release v0.1.0"
git push origin v0.1.0
```

On GitHub:
- [ ] Go to "Releases"
- [ ] Click "Create a new release"
- [ ] Select tag `v0.1.0`
- [ ] Title: "v0.1.0 - Initial Release"
- [ ] Description: Copy from CHANGELOG.md
- [ ] Publish release

## Post-Deployment Checklist

### 1. Verify Installation
- [ ] Clone from GitHub to fresh directory
- [ ] Follow QUICKSTART.md exactly
- [ ] Test with real Pulseway credentials
- [ ] Verify all tools work in Claude Desktop

### 2. Documentation
- [ ] Update repository URL in README.md
- [ ] Update repository URL in CONTRIBUTING.md
- [ ] Update repository URL in PROJECT_SUMMARY.md
- [ ] Update repository URL in pyproject.toml

### 3. Community
- [ ] Add CONTRIBUTING.md guidelines
- [ ] Add issue templates (optional)
- [ ] Add pull request template (optional)
- [ ] Add CODE_OF_CONDUCT.md (optional)

### 4. Promotion (Optional)
- [ ] Share on social media
- [ ] Post in relevant communities
- [ ] Add to MCP server directory
- [ ] Write a blog post

## Quick Security Audit

Run this before pushing to GitHub:

```bash
# Check for potential secrets in code
grep -r "password\|secret\|api_key\|token" --include="*.py" --include="*.md" pulseway_mcp_server/

# Verify .gitignore is working
git status --ignored

# Check what will be pushed
git diff --cached

# List all tracked files
git ls-files
```

**CRITICAL**: Ensure `secrets.env` is NEVER listed in `git ls-files`!

## Emergency: Secrets Accidentally Committed

If you accidentally commit secrets:

```bash
# Remove from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch secrets.env' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (destructive!)
git push origin --force --all

# Immediately rotate all credentials in Pulseway
# Generate new passwords/tokens
```

Better: Don't commit secrets in the first place!

## Common Issues

### "Permission denied" on push
- Check SSH keys or HTTPS credentials
- Verify repository access permissions

### CI workflow fails
- Check Python version compatibility
- Verify all dependencies are in pyproject.toml
- Check GitHub Actions secrets if needed

### Tests fail locally
- Ensure `secrets.env` is not configured (tests use mocks)
- Run `uv pip install -e ".[dev]"` to get test dependencies
- Check Python version (3.10+ required)

## Success Criteria

Your deployment is successful when:
- ✅ Repository is public/accessible
- ✅ CI/CD passes all tests
- ✅ README renders correctly on GitHub
- ✅ Someone else can clone and install following QUICKSTART.md
- ✅ No secrets are in the repository
- ✅ GitHub Actions badge is green

## Deployment Complete! 🎉

Once all items are checked, your Pulseway MCP Server is ready for the world!

Next steps:
1. Monitor GitHub Actions for any issues
2. Watch for issues from users
3. Plan future features
4. Keep dependencies updated
