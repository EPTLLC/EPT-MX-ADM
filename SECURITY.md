# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**We do not provide support or security response.**

This project is released AS-IS without warranties or guarantees.

However, if you discover a critical security vulnerability:

1. **DO NOT** open a public issue
2. Contact: mail.easypro.tech@gmail.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (optional)

**Note:** Response is not guaranteed. Consider forking and fixing if urgent.

## Security Best Practices

### Deployment

1. **Never run as root**
   ```bash
   useradd -r -s /bin/bash matrix-admin
   sudo -u matrix-admin python app.py
   ```

2. **Use reverse proxy with HTTPS**
   - Nginx/Apache with Let's Encrypt
   - Terminate SSL at proxy level
   - Set proper headers (HSTS, CSP, X-Frame-Options)

3. **Restrict network access**
   ```bash
   # Bind to localhost only
   gunicorn -b 127.0.0.1:5000 app:app
   ```

4. **File permissions**
   ```bash
   chmod 755 /opt/ept-mx-adm
   chmod 644 /opt/ept-mx-adm/*.py
   chmod 600 /opt/ept-mx-adm/config.json
   ```

### Configuration

1. **Disable debug mode in production**
   ```json
   {
     "debug": false
   }
   ```

2. **Use strong admin passwords**
   - Minimum 16 characters
   - Mixed case, numbers, symbols
   - Use password manager

3. **Regularly update dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   pip-audit
   ```

### Secrets Management

1. **NEVER commit secrets to git**
   - API tokens
   - Passwords
   - Private keys
   - Session secrets

2. **Use environment variables**
   ```bash
   export FLASK_SECRET_KEY=$(openssl rand -hex 32)
   ```

3. **Use .pypirc.example template**
   ```bash
   cp .pypirc.example ~/.pypirc
   chmod 600 ~/.pypirc
   # Edit and add your token
   ```

### Monitoring

1. **Check logs regularly**
   ```bash
   tail -f logs/app.log
   grep ERROR logs/app.log
   ```

2. **Monitor failed login attempts**
   - Look for patterns in logs
   - Consider rate limiting

3. **Audit admin actions**
   - User modifications
   - Room deletions
   - Media operations

## Known Security Considerations

### 1. SSL Verification Disabled

**Location:** `modules/auth.py`

**Reason:** Support for self-signed certificates

**Risk:** Man-in-the-middle attacks possible

**Mitigation:** Use proper SSL certificates in production

### 2. No CSRF Protection

**Status:** Flask sessions without CSRF tokens

**Risk:** Cross-site request forgery

**Mitigation:** Planned for v1.1.0 (Flask-WTF integration)

### 3. No Rate Limiting

**Status:** No login attempt throttling

**Risk:** Brute force attacks

**Mitigation:** Use reverse proxy rate limiting (nginx limit_req)

### 4. Session Security

**Status:** Flask default session management

**Risk:** Session hijacking if SECRET_KEY is weak

**Mitigation:** 
- Set strong SECRET_KEY in config
- Use HTTPS only
- Set secure cookie flags

### 5. Input Validation

**Status:** Basic validation, relies on Synapse API

**Risk:** Injection attacks if Synapse API has vulnerabilities

**Mitigation:** Keep Synapse updated, validate all inputs

## Security Scanning

### Automated Scans

```bash
# Secret detection
detect-secrets scan --all-files

# Dependency vulnerabilities
pip-audit
safety check

# Code security
bandit -r . -x ./venv,./tests

# Static analysis
flake8 .
```

### Manual Review

- [ ] Review all admin privilege checks
- [ ] Audit session management
- [ ] Check input sanitization
- [ ] Verify API authentication
- [ ] Test authorization boundaries
- [ ] Review error messages (no info leakage)
- [ ] Check logging (no sensitive data)

## Security Tools

This project uses:

- **detect-secrets**: Secret scanning (`.secrets.baseline`)
- **bandit**: Python security linter
- **pip-audit**: Dependency vulnerability scanning
- **flake8**: Code quality and security patterns
- **Dependabot**: Automated dependency updates (GitHub)

## Updates and Patches

Security-related changes will be noted in `CHANGELOG.md` with `[SECURITY]` prefix.

No dedicated security mailing list or notifications provided.

Monitor:
- GitHub releases: https://github.com/EPTLLC/EPT-MX-ADM/releases
- PyPI updates: https://pypi.org/project/ept-mx-adm/

## Disclaimer

**NO WARRANTIES:** This software is provided "as is" without warranty of any kind.

**NO LIABILITY:** The authors are not liable for any damages arising from use.

**NO SUPPORT:** Security support is not provided.

Use at your own risk. Conduct your own security assessment before production deployment.

---

**Last Updated:** October 24, 2025
**Version:** 1.0.1

