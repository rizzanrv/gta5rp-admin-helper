# Security Policy

## Supported Versions

Currently supported versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please follow these steps:

1. **Do NOT** open a public issue
2. Send a detailed report via Telegram: [@unbrokenflex](https://t.me/unbrokenflex)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to expect

- Acknowledgment of your report within 48 hours
- Regular updates on the progress
- Credit in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices

When using this application:

1. **API Keys**: Never commit your `.env` file or share your OCR API key
2. **Database**: The `reports.db` file contains your statistics - keep it secure
3. **Updates**: Keep the application and dependencies up to date
4. **Permissions**: The application requires:
   - Screen capture permissions
   - Keyboard input monitoring
   - Network access for OCR API calls

## Known Security Considerations

- The application captures screenshots which may contain sensitive information
- Global keyboard listener monitors Enter key presses system-wide
- OCR API requests send screenshot data to external service
- Temporary screenshot files are created and deleted (may persist on disk briefly)

## Dependencies

We regularly monitor and update dependencies for security vulnerabilities. You can check for updates:

```bash
pip list --outdated
```

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
```
