# Troubleshooting Guide

Common issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [CLI Issues](#cli-issues)
- [API Issues](#api-issues)
- [Integration Issues](#integration-issues)
- [Performance Issues](#performance-issues)
- [Configuration Issues](#configuration-issues)

## Installation Issues

### Issue: `ModuleNotFoundError: No module named 'sspm_engine'`

**Symptoms:**
```
ModuleNotFoundError: No module named 'sspm_engine'
```

**Causes:**
- Package not installed
- Wrong virtual environment
- Incorrect Python path

**Solutions:**

1. **Verify virtual environment is activated:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Reinstall the package:**
```bash
pip install -e .
```

3. **Check Python path:**
```bash
which python  # Should point to your venv
python -c "import sspm_engine; print(sspm_engine.__file__)"
```

---

### Issue: `pip install` fails with dependency conflicts

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
```

**Solutions:**

1. **Create a fresh virtual environment:**
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e .
```

2. **Use specific Python version:**
```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -e .
```

3. **Install with --no-deps flag (advanced):**
```bash
pip install --no-deps -e .
pip install -r requirements.txt
```

---

### Issue: `PyYAML` build fails

**Symptoms:**
```
ERROR: Failed to build 'pyyaml' when getting requirements to build wheel
```

**Solutions:**

1. **Update PyYAML version in requirements.txt:**
```bash
# Change pyyaml>=5.4.1 to pyyaml>=6.0
pip install pyyaml>=6.0
```

2. **Install system dependencies (Linux):**
```bash
sudo apt-get install python3-dev libyaml-dev
```

3. **Install system dependencies (macOS):**
```bash
brew install libyaml
```

---

## CLI Issues

### Issue: `sspmctl: command not found`

**Symptoms:**
```
(eval):1: command not found: sspmctl
```

**Causes:**
- Console script not installed
- PATH not updated
- Virtual environment issue

**Solutions:**

1. **Use module path instead:**
```bash
python -m sspm_engine.cli.sspmctl --help
```

2. **Reinstall with entry points:**
```bash
pip uninstall sspm-engine
pip install -e .
```

3. **Check if script exists:**
```bash
find venv -name "sspmctl*"
```

4. **Add to PATH (if found):**
```bash
export PATH="$PATH:$(pwd)/venv/bin"
```

---

### Issue: CLI hangs or freezes

**Symptoms:**
- Command runs but never completes
- No output or progress indicator

**Causes:**
- API timeout
- Network issues
- Large dataset

**Solutions:**

1. **Check network connectivity:**
```bash
curl https://api.github.com
curl https://slack.com/api/auth.test
```

2. **Increase timeout in config:**
```yaml
# config/settings.yaml
api:
  timeout: 300  # 5 minutes
```

3. **Scan providers individually:**
```bash
python -m sspm_engine.cli.sspmctl scan slack
python -m sspm_engine.cli.sspmctl scan github
python -m sspm_engine.cli.sspmctl scan google
```

4. **Enable debug logging:**
```bash
export LOG_LEVEL=DEBUG
python -m sspm_engine.cli.sspmctl scan all
```

---

## API Issues

### Issue: API server won't start

**Symptoms:**
```
ERROR: [Errno 48] Address already in use
```

**Solutions:**

1. **Check if port is in use:**
```bash
lsof -i :8000
```

2. **Kill existing process:**
```bash
kill -9 <PID>
```

3. **Use different port:**
```bash
uvicorn sspm_engine.api.server:app --port 8001
```

---

### Issue: API returns 500 Internal Server Error

**Symptoms:**
```json
{
  "detail": "Internal Server Error"
}
```

**Solutions:**

1. **Check server logs:**
```bash
uvicorn sspm_engine.api.server:app --log-level debug
```

2. **Verify configuration files exist:**
```bash
ls -la sspm_engine/config/
```

3. **Test with mock data:**
```bash
unset SLACK_BOT_TOKEN
unset GITHUB_TOKEN
unset GOOGLE_SA_KEY_PATH
uvicorn sspm_engine.api.server:app --reload
```

---

### Issue: API timeout on large scans

**Symptoms:**
- Request times out after 30 seconds
- Incomplete results

**Solutions:**

1. **Increase client timeout:**
```bash
curl --max-time 300 -X POST "http://localhost:8000/scan/all"
```

2. **Use async scanning (Python):**
```python
import asyncio
import aiohttp

async def scan():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:
        async with session.post("http://localhost:8000/scan/all") as response:
            return await response.json()

results = asyncio.run(scan())
```

3. **Scan providers separately:**
```bash
curl -X POST "http://localhost:8000/scan/slack"
curl -X POST "http://localhost:8000/scan/github"
curl -X POST "http://localhost:8000/scan/google"
```

---

## Integration Issues

### Issue: Slack authentication fails

**Symptoms:**
```
slack_sdk.errors.SlackApiError: The request to the Slack API failed.
```

**Causes:**
- Invalid token
- Missing scopes
- Token expired

**Solutions:**

1. **Verify token:**
```bash
curl -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test
```

2. **Check required scopes:**
Required: `users:read`, `channels:read`, `groups:read`

3. **Regenerate token:**
- Go to api.slack.com/apps
- Select your app
- Navigate to "OAuth & Permissions"
- Reinstall the app

4. **Test with mock data:**
```bash
unset SLACK_BOT_TOKEN
python -m sspm_engine.cli.sspmctl scan slack
```

---

### Issue: GitHub rate limit exceeded

**Symptoms:**
```
github.GithubException.RateLimitExceededException: 403 API rate limit exceeded
```

**Solutions:**

1. **Check rate limit status:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

2. **Wait for reset:**
```python
import time
from github import Github

g = Github(os.getenv("GITHUB_TOKEN"))
rate_limit = g.get_rate_limit()
reset_time = rate_limit.core.reset
wait_seconds = (reset_time - time.time())
print(f"Wait {wait_seconds} seconds")
```

3. **Use authenticated requests:**
Ensure `GITHUB_TOKEN` is set (increases limit from 60 to 5000 requests/hour)

4. **Implement caching:**
```python
# Cache results for 1 hour
import time
cache = {}
cache_time = 3600

def get_repos():
    if 'repos' in cache and time.time() - cache['time'] < cache_time:
        return cache['repos']
    repos = github.fetch_data()
    cache['repos'] = repos
    cache['time'] = time.time()
    return repos
```

---

### Issue: Google Workspace authentication fails

**Symptoms:**
```
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials.
```

**Causes:**
- Service account key not found
- Invalid JSON key file
- Missing domain-wide delegation

**Solutions:**

1. **Verify key file exists:**
```bash
ls -la $GOOGLE_SA_KEY_PATH
cat $GOOGLE_SA_KEY_PATH | jq .
```

2. **Check file permissions:**
```bash
chmod 600 $GOOGLE_SA_KEY_PATH
```

3. **Validate JSON structure:**
```bash
python -c "import json; json.load(open('$GOOGLE_SA_KEY_PATH'))"
```

4. **Enable domain-wide delegation:**
- Go to console.cloud.google.com
- Navigate to IAM & Admin → Service Accounts
- Edit service account
- Enable "Enable Google Workspace Domain-wide Delegation"

5. **Authorize in Admin Console:**
- Go to admin.google.com
- Security → API Controls → Domain-wide Delegation
- Add client ID and scopes

---

## Performance Issues

### Issue: Scans are very slow

**Symptoms:**
- Scan takes more than 5 minutes
- High memory usage
- CPU at 100%

**Solutions:**

1. **Scan providers in parallel:**
```bash
#!/bin/bash
python -m sspm_engine.cli.sspmctl scan slack &
python -m sspm_engine.cli.sspmctl scan github &
python -m sspm_engine.cli.sspmctl scan google &
wait
```

2. **Reduce dataset size:**
```yaml
# config/settings.yaml
limits:
  max_users: 1000
  max_repos: 100
  max_files: 500
```

3. **Disable unused scanners:**
```yaml
# config/settings.yaml
scanners:
  permissions:
    enabled: true
  external_access:
    enabled: true
  misconfig:
    enabled: false  # Disable if not needed
  secret_scanner:
    enabled: false  # Disable if not needed
```

4. **Use caching:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(data):
    # Your code here
    pass
```

---

### Issue: High memory usage

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**

1. **Process data in chunks:**
```python
def process_in_chunks(data, chunk_size=100):
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        yield process_chunk(chunk)
```

2. **Use generators instead of lists:**
```python
# Instead of:
results = [process(item) for item in large_list]

# Use:
results = (process(item) for item in large_list)
```

3. **Clear cache periodically:**
```python
import gc
gc.collect()
```

---

## Configuration Issues

### Issue: Configuration file not found

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'config/settings.yaml'
```

**Solutions:**

1. **Check file exists:**
```bash
ls -la sspm_engine/config/
```

2. **Use absolute path:**
```python
import os
config_path = os.path.join(os.path.dirname(__file__), "config", "settings.yaml")
engine = SSPMEngine(config_path=config_path)
```

3. **Create default config:**
```bash
mkdir -p sspm_engine/config
cp examples/settings.yaml.example sspm_engine/config/settings.yaml
```

---

### Issue: Invalid YAML syntax

**Symptoms:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solutions:**

1. **Validate YAML:**
```bash
python -c "import yaml; yaml.safe_load(open('config/settings.yaml'))"
```

2. **Check indentation:**
YAML requires consistent indentation (use spaces, not tabs)

```yaml
# Correct:
scanners:
  permissions:
    enabled: true

# Incorrect:
scanners:
permissions:  # Wrong indentation
  enabled: true
```

3. **Use online validator:**
http://www.yamllint.com/

---

## Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
export LOG_LEVEL=DEBUG
python -m sspm_engine.cli.sspmctl scan all
```

Or in Python:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from sspm_engine.engine import SSPMEngine
engine = SSPMEngine()
results = engine.run_scan("all")
```

---

## Getting Help

If you're still experiencing issues:

1. **Check existing issues:**
   https://github.com/Raoof128/SSPME/issues

2. **Create a new issue:**
   Include:
   - Python version (`python --version`)
   - OS and version
   - Full error message
   - Steps to reproduce
   - Configuration (remove sensitive data)

3. **Join discussions:**
   https://github.com/Raoof128/SSPME/discussions

---

## Common Error Messages

### `ImportError: cannot import name 'X' from 'sspm_engine'`

**Solution:** Reinstall the package:
```bash
pip install -e . --force-reinstall
```

### `TypeError: 'NoneType' object is not iterable`

**Solution:** Check if API returned data:
```python
data = integration.fetch_data()
if data is None:
    print("No data returned from API")
```

### `JSONDecodeError: Expecting value`

**Solution:** Verify API response format:
```bash
curl -v http://localhost:8000/scan/all
```

### `PermissionError: [Errno 13] Permission denied`

**Solution:** Check file permissions:
```bash
chmod +r config/settings.yaml
chmod +r config/risk_rules.json
```

---

## Next Steps

- [Configuration Guide](CONFIGURATION.md)
- [Usage Guide](USAGE.md)
- [API Reference](API_REFERENCE.md)
- [Contributing](../CONTRIBUTING.md)

