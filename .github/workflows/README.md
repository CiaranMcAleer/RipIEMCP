# GitHub Actions Test Validation

This directory contains GitHub Actions workflows for automated testing and validation of the RIP.ie MCP Server.

## Workflows

### `test.yml` - Main Test Suite
- **Triggers**: Push to main/develop, Pull requests to main
- **Python Versions**: 3.7, 3.8, 3.9, 3.10, 3.11
- **Tests**:
  - Server startup validation
  - MCP protocol compliance tests
  - Tool discovery and schema validation
  - Individual tool handler testing
  - Integration tests

### `security.yml` - Security and Dependencies
- **Triggers**: Monthly schedule, changes to requirements.txt
- **Features**:
  - Security vulnerability scanning with `safety` and `bandit`
  - Dependency audit with `pip-audit`
  - Requirements validation across Python versions
  - Automated security reports

## Test Results

The workflows generate detailed test reports that appear in:
- GitHub Actions summary pages
- Pull request checks
- Workflow artifacts for security reports

## Setup

These workflows are automatically triggered when:
1. Code is pushed to `main` or `develop` branches
2. Pull requests are opened against `main`
3. `requirements.txt` is modified
4. Monthly security scans (1st of each month at 8 AM GMT)

## Local Testing

To run tests locally before pushing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test suite
python test_rip_ie_mcp.py

# Check code formatting (if you have black installed)
pip install black flake8
black --check rip-ie-server/rip_ie_server.py test_rip_ie_mcp.py
flake8 rip-ie-server/rip_ie_server.py --max-line-length=100

# Security scan (if you have the tools installed)
pip install safety bandit
safety check
bandit -r rip-ie-server/
```

## Badge Status

The README includes status badges that show:
- ✅ Green: All tests passing
- ❌ Red: Tests failing
- 🟡 Yellow: Tests in progress

Click the badges to view detailed test results and logs.