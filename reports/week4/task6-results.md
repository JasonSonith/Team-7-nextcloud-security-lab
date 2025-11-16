# Task 6 — Week 4 Summary & Recommendations

## Summary of Findings

### Task 4 — Path Traversal
- We successfully wrote a file (`evil.txt`) **outside** the intended Nextcloud storage directory.
- This confirms a **path traversal vulnerability**.
- This allows attackers to write files outside the allowed location.

### Task 5 — Remote Code Execution (RCE) Attempt
- A PHP webshell (`shell.php`) was uploaded.
- Multiple execution paths were tested.
- All attempts returned "Page not found" and *no PHP code executed*.
- This confirms Nextcloud **blocked remote code execution** via uploaded files.

---

## Security Impact

- **Path Traversal (Task 4): HIGH RISK**  
  Attackers can escape the data directory and potentially overwrite system files.

- **RCE (Task 5): LOW RISK**  
  Nextcloud correctly prevents execution of uploaded PHP files.

---

## Recommendations

1. **Sanitize file paths** to prevent `../` traversal.
2. **Enforce allowed paths** using absolute paths instead of user-supplied paths.
3. **Disable direct filesystem access** unless strictly needed.
4. **Use container-level file system permissions** to keep the Nextcloud web user jailed.
5. **Monitor logs** for suspicious upload patterns.

---

## Conclusion

- The system is **vulnerable to directory traversal**.
- The system is **not vulnerable to direct RCE** through file upload.
- Fixing path traversal should be a priority, since it could enable future RCE or privilege escalation.


