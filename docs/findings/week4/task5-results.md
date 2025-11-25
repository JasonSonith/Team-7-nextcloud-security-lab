# Task 5 – Special Character Filename Handling  
**Nextcloud Security Lab – Week 4**

## 🔍 Overview
This task tested how Nextcloud handles unusual, unsafe, or malformed filenames.  
The goal was to determine whether filename parsing could cause errors, uploads to bypass validation, or security issues.

---

## ✅ 1. Unicode & Emoji Filenames
**Files tested:**
- `file-😀-emoji.txt`
- `file-中文.txt`
- `файл.txt` (Cyrillic)

**Observed Behavior:**
- All uploaded successfully through the web UI  
- Displayed properly in the file list  
- No corruption or renaming  
- Downloading the files works normally

**Conclusion:**  
Nextcloud fully supports Unicode and emoji filenames.  
❌ No vulnerability found  
✔ Good internationalization support

---

## ⚠️ 2. Reserved/Special Characters
**Files tested:**
- `file:name.txt`
- `file<name>.txt`
- `file|name.txt`
- `file*.txt`

**Observed Behavior:**
- All files uploaded successfully  
- Nextcloud did *not* block or sanitize the names  
- UI showed them just like normal files  
- These characters are normally **forbidden on Windows systems**

**Conclusion:**  
Nextcloud accepts characters that Windows cannot handle.  
⚠ This may cause:
- Sync conflicts  
- Errors when downloading on Windows  
- Problems when zipping/exporting files

**Risk Level:** Low (interoperability issue, not a security issue)

---

## ❌ 3. Long Filename Test
**Filename Attempt:**
- `A` repeated 255–300 times (Linux allows max 255 chars)

**Observed Behavior:**
- Linux allowed creation of a 255-character filename  
- Nextcloud rejected upload of both long filenames  
- The UI displayed: **“Error during upload: File name is too long”**

**Conclusion:**  
This is correct behavior.  
✔ Server enforced filename length limits  
✔ Prevented storage corruption  
❌ Does not auto-truncate (just blocks upload)

---

## ⚠️ 4. Null Byte Injection Attempt
**Filename tested:**
- `test%00.txt.php`

**Observed Behavior:**
- Uploaded successfully  
- Filename stored exactly as `test%00.txt.php`  
- `%00` treated as literal characters  
- No splitting, no parsing errors  
- The file was **not executed** as PHP (correct behavior)

**Conclusion:**  
Null byte injection is not possible.  
Nextcloud properly sanitizes/escapes null bytes.

---

## 📌 Summary of All Findings

| Test Type | Result | Notes |
|----------|--------|-------|
| Unicode / Emoji | ✅ Passed | Fully supported, safe |
| Reserved Characters | ⚠️ Mixed | Allowed, but may break Windows sync |
| Long Filenames | ❌ Blocked | Proper length enforcement |
| Null Byte Injection | ✅ Safe | Null byte not interpreted |

---

## 📁 Evidence
Screenshots stored in:  
`docs/evidence/week4/file-upload-testing/special-chars/`

---

## 🏁 Final Assessment
Nextcloud handled all dangerous filename cases safely, except for allowing Windows-reserved characters, which may cause interoperability problems but not security vulnerabilities.
