# Security Guidelines for GenAI Stack

## 🔐 API Key Security

### Environment Variables
- **NEVER** commit API keys directly in code
- **ALWAYS** use environment variables for sensitive data
- **ALWAYS** add `.env` files to `.gitignore`

### Required Environment Variables
```bash
# API Keys (Required)
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your_very_strong_secret_key_here
```

## 🛡️ Security Best Practices

### 1. API Key Management
- Use different API keys for development and production
- Rotate API keys regularly
- Monitor API key usage and set up alerts
- Use API key restrictions when possible

### 2. Database Security
- Use strong passwords for database connections
- Enable SSL/TLS for database connections in production
- Regularly update database software
- Use connection pooling and rate limiting

### 3. Application Security
- Keep dependencies updated
- Use HTTPS in production
- Implement proper CORS policies
- Validate all user inputs
- Use rate limiting for API endpoints

### 4. File Upload Security
- Validate file types and sizes
- Scan uploaded files for malware
- Store uploaded files outside web root
- Use secure file naming conventions

## 🚨 Security Checklist

### Before Deployment
- [ ] All API keys are in environment variables
- [ ] `.env` files are in `.gitignore`
- [ ] Database credentials are secure
- [ ] HTTPS is enabled
- [ ] CORS is properly configured
- [ ] File uploads are validated
- [ ] Dependencies are updated
- [ ] Security headers are set

### Regular Maintenance
- [ ] Rotate API keys monthly
- [ ] Update dependencies weekly
- [ ] Monitor logs for suspicious activity
- [ ] Review access permissions quarterly
- [ ] Backup data regularly

## 🔍 Security Monitoring

### Log Monitoring
- Monitor API key usage
- Track failed authentication attempts
- Log file upload activities
- Monitor database queries

### Alerts
- Set up alerts for unusual API usage
- Monitor for failed login attempts
- Track file upload anomalies
- Alert on database connection issues

## 🚫 Common Security Mistakes

### ❌ Don't Do This
```python
# NEVER hardcode API keys
openai_api_key = "sk-proj-abc123..."

# NEVER commit .env files
git add .env

# NEVER use weak secrets
SECRET_KEY = "password123"
```

### ✅ Do This Instead
```python
# Use environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Add to .gitignore
echo ".env" >> .gitignore

# Use strong secrets
SECRET_KEY = generate_secure_key()
```

## 🔧 Security Tools

### Recommended Tools
- **Secret Scanning**: GitHub Secret Scanning, GitGuardian
- **Dependency Scanning**: Snyk, OWASP Dependency Check
- **Code Analysis**: SonarQube, CodeQL
- **Vulnerability Scanning**: Nessus, OpenVAS

### Environment Setup
```bash
# Run the secure setup script
python setup-env.py

# Verify .gitignore
cat .gitignore | grep -E "\.env|secrets|keys"

# Check for exposed secrets
grep -r "sk-proj\|AIza\|api_key" --exclude-dir=node_modules .
```

## 📞 Incident Response

### If API Keys Are Compromised
1. **Immediately** rotate the compromised keys
2. **Review** access logs for unauthorized usage
3. **Update** all environment variables
4. **Notify** team members
5. **Monitor** for continued unauthorized access

### If Database Is Compromised
1. **Immediately** change database passwords
2. **Review** database access logs
3. **Check** for data exfiltration
4. **Update** application credentials
5. **Notify** affected users if necessary

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)
- [Environment Variable Security](https://12factor.net/config)
- [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

## 🤝 Reporting Security Issues

If you discover a security vulnerability, please:
1. **DO NOT** create a public issue
2. **Email** security concerns to: security@yourdomain.com
3. **Include** detailed information about the vulnerability
4. **Wait** for confirmation before public disclosure

---

**Remember**: Security is everyone's responsibility. When in doubt, ask for help!
