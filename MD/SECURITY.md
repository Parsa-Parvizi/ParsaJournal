# Security Configuration Guide for Parsa Journal

## Admin Panel Security

### Custom Admin URL
Change the default admin URL for better security:
```bash
# In .env file
ADMIN_URL=your-custom-admin-url
```

### IP Whitelist
Restrict admin access to specific IP addresses:
```bash
# In .env file
ADMIN_IP_WHITELIST=127.0.0.1,::1,your-ip-address
```

### Rate Limiting
The admin panel has built-in rate limiting:
- 5 login attempts per 15 minutes per IP
- Automatic blocking after exceeding limits
- Logs all login attempts

### Security Features

1. **Custom Admin Site**
   - Enhanced permission checks
   - IP-based access control
   - Login attempt logging
   - Suspicious activity monitoring

2. **Admin Security Middleware**
   - Rate limiting for login attempts
   - IP whitelisting
   - Access logging
   - Automatic blocking

3. **Session Security**
   - Secure session cookies
   - HttpOnly cookies
   - Session timeout configuration
   - Secure cookie flags in production

4. **Logging**
   - All admin access attempts logged
   - Failed login attempts logged
   - Suspicious activity alerts
   - Log files in `logs/` directory

## Database Security

### PostgreSQL Configuration

1. **Strong Passwords**
   ```bash
   # Use strong, unique passwords
   DB_PASSWORD=your-strong-password-here
   ```

2. **Connection Security**
   - Use SSL connections in production
   - Restrict database access by IP
   - Use connection pooling
   - Set connection timeouts

3. **Backup Security**
   - Encrypt database backups
   - Store backups securely
   - Regular backup schedule
   - Test backup restoration

## Environment Variables Security

### Secret Key
```bash
# Generate a strong secret key
SECRET_KEY=your-very-long-random-secret-key-here
```

### Production Settings
```bash
# In production .env
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## HTTPS Configuration

1. **SSL Certificates**
   - Use Let's Encrypt for free SSL
   - Configure in nginx.conf
   - Enable HSTS
   - Redirect HTTP to HTTPS

2. **Security Headers**
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - X-XSS-Protection: 1; mode=block
   - Referrer-Policy: strict-origin-when-cross-origin

## File Upload Security

1. **Image Validation**
   - File type validation
   - File size limits
   - Image dimension checks
   - Virus scanning (optional)

2. **Media Files**
   - Store outside web root
   - Restrict access
   - Use CDN for production
   - Regular cleanup

## Django Security Settings

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags
- [ ] Configure CSRF protection
- [ ] Enable XSS protection
- [ ] Set up logging
- [ ] Configure backups
- [ ] Set up monitoring

## Monitoring and Alerts

1. **Log Monitoring**
   - Monitor admin access logs
   - Track failed login attempts
   - Alert on suspicious activity
   - Regular log review

2. **Security Alerts**
   - Failed login attempts
   - Unauthorized access attempts
   - Rate limit violations
   - Database connection issues

## Best Practices

1. **Regular Updates**
   - Keep Django updated
   - Update dependencies
   - Apply security patches
   - Monitor security advisories

2. **Access Control**
   - Use strong passwords
   - Enable two-factor authentication (if available)
   - Limit admin access
   - Regular access review

3. **Backup Strategy**
   - Regular database backups
   - Test backup restoration
   - Store backups securely
   - Document backup procedures

4. **Incident Response**
   - Document security incidents
   - Have a response plan
   - Regular security audits
   - Keep security logs

## Additional Security Measures

1. **Firewall Configuration**
   - Restrict database port access
   - Allow only necessary ports
   - Use VPN for admin access
   - Configure IP restrictions

2. **Docker Security**
   - Use non-root user in containers
   - Limit container resources
   - Scan images for vulnerabilities
   - Keep images updated

3. **Network Security**
   - Use private networks
   - Encrypt traffic
   - Monitor network activity
   - Use VPN for remote access

## Security Testing

1. **Regular Audits**
   - Security vulnerability scans
   - Penetration testing
   - Code reviews
   - Dependency checks

2. **Monitoring Tools**
   - Log aggregation
   - Intrusion detection
   - Performance monitoring
   - Error tracking

## Contact

For security issues, please contact through the website contact form.

