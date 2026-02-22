# Secure Masking Utility v3.1 🛡️

A portable, air-gapped data sanitization tool for local PII processing.

## 🚀 Core Features
* **Zero-Network Architecture:** 100% offline processing; no external data transmission.
* **Salted HMAC-SHA256:** Deterministic hashing for referential integrity across datasets.
* **Auto-PII Detection:** Automated scanning for sensitive headers (ID, Name, Passport, etc.).
* **Memory Hygiene:** RAM-only processing with active memory wiping post-execution.
* **Audit Logs:** Generates a text-based Audit Report with record counts for every run.

## 🛠️ Build Instructions
1. Ensure `pandas`, `openpyxl`, and `pyinstaller` are installed.
2. Build the executable:
`pyinstaller --onefile --noconsole --icon=securemasker.ico --add-data "securemasker.ico;." --name Secure_Masking_Utility masker.py`

## ⚖️ License
MIT License - Developed by Shazily Munawar.
