# Task 5 — PHP Shell Upload Test

## PHP Upload Execution Test
A simple PHP shell file named `shell.php` was created with the following code:

<?php echo 'Hacked'; ?>

This file was uploaded to Nextcloud using the web interface.

---

## Execution Attempts
We attempted to access and execute the uploaded PHP file using several possible paths:

- http://localhost:8080/shell.php
- http://localhost:8080/data/shell.php
- http://localhost:8080/remote.php/webdav/shell.php
- http://localhost:8080/apps/files/shell.php

### Actual Behavior
All requests returned “Page not found” and the PHP code was **not executed**.

### Expected Behavior
Nextcloud should prevent the execution of any user-uploaded PHP files.  
These files should only be downloadable, never runnable.

---

## Conclusion
Nextcloud successfully blocked execution of the uploaded PHP file.  
This confirms that the platform properly mitigates Remote Code Execution (RCE) by preventing execution of untrusted file uploads.  
While the system is vulnerable to path traversal (Task 4), it is **not** vulnerable to PHP web-shell execution through normal uploads.

