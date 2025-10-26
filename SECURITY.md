# Security Policy

## 🔒 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## 🐛 Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to: security@yourdomain.com

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

## 🛡️ Security Measures

MERCUR-E implements the following security measures:

### Webhook Security
- ✅ HMAC-SHA256 signature validation
- ✅ Constant-time comparison to prevent timing attacks
- ✅ Signature verification for all incoming webhooks

### Authentication
- ✅ JWT-based GitHub App authentication
- ✅ Installation token management with expiration
- ✅ Optional PAM authentication for privileged operations

### Network Security
- ✅ TLS/HTTPS support
- ✅ Rate limiting via nginx
- ✅ CORS configuration
- ✅ Security headers (HSTS, X-Frame-Options, etc.)

### Code Security
- ✅ No file deletion permissions
- ✅ Input validation
- ✅ Secure secret storage
- ✅ No hardcoded credentials

### Deployment Security
- ✅ Non-root Docker user
- ✅ Read-only volume mounts for sensitive files
- ✅ Environment-based configuration
- ✅ Minimal Docker image

## 🔐 Best Practices

When deploying MERCUR-E:

1. **Never commit secrets** - Use environment variables
2. **Rotate webhook secrets** regularly
3. **Use strong secrets** - Generate with `openssl rand -hex 32`
4. **Enable TLS** in production
5. **Keep dependencies updated**
6. **Monitor logs** for suspicious activity
7. **Limit GitHub App permissions** to minimum required
8. **Use firewall rules** to restrict access
9. **Regular security audits**
10. **Keep private key secure** - chmod 600

## 📝 Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find any similar problems
3. Prepare fixes for all supported versions
4. Release new versions as soon as possible

## 🙏 Acknowledgments

We appreciate the security research community's efforts in responsibly disclosing vulnerabilities.

---

**Last Updated:** October 26, 2024
