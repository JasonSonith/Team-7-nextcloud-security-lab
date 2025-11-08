  ## Current State Assessment

  ### Secrets Identified
  - Database credentials (MariaDB)
  - Nextcloud admin credentials
  - TLS private key (lab.key)
  - Application secrets

  ### Current Storage Methods
  - Plaintext in .env files
  - Filesystem storage for TLS keys
  - No encryption at rest
  - No automated rotation

  ## Recommendations

  ### For Lab Environment
  1. Keep .env in .gitignore (already done)
  2. TLS key permissions: chmod 600 (already done)
  3. Document: DO NOT use this setup in production

  ### For Production Environment

  #### 1. Secret Management
  **Use:** HashiCorp Vault or AWS Secrets Manager
  - Store all credentials encrypted
  - Enable automatic rotation
  - Audit all secret access

  #### 2. TLS Certificate Management
  **Use:** Let's Encrypt with cert-bot or AWS Certificate Manager
  - Automated renewal every 60-90 days
  - Valid CA-signed certificates
  - Store private keys in HSM if possible

  #### 3. Database Credentials
  - Use unique passwords per service (not root for app)
  - Rotate every 90 days minimum
  - Use IAM roles where possible (cloud deployments)

  #### 4. Encryption Keys (if using Nextcloud encryption)
  - Store master keys in external KMS
  - Never store encryption keys on same host as encrypted data
  - Implement key rotation policy

  #### 5. Access Control
  - Principle of least privilege
  - Separate keys per environment (dev/staging/prod)
  - Audit logs for all key access

  ## Implementation Priority

  1. **Immediate:** Move to proper secret manager (Vault/KMS)
  2. **Week 1:** Implement TLS with Let's Encrypt
  3. **Week 2:** Set up key rotation policies
  4. **Week 3:** Implement monitoring and alerts
  5. **Ongoing:** Regular security audits

  ## Evidence
  - See: scans/nmap-ssl-enum.txt (TLS configuration)
  - See: infra/docker/.env.example (secret template)
  - See: threat-model/STRIDE.md (threat analysis)