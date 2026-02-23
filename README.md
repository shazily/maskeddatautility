# Secure Masking Utility v3.2.4 🛡️

A tactical, air-gapped data sanitization tool built to bridge the gap between manual data environments and enterprise-scale pipelines.

## 🚀 The Philosophy: Code to the Data
Data masking is notoriously complex in large-scale environments, often slowed down by a heavy "Compliance Tax"—weeks of approvals and infrastructure overhead. For pilots, tactical solutions, or manual datasets on user-end environments, waiting for a massive enterprise pipeline is a bottleneck.

**This utility simplifies the process by bringing the sanitization logic directly to the source.**

## ✨ Features
* **Zero-Network Architecture:** 100% offline; no external data transmission.
* **Persistent Audit History:** Automatically creates an `/Audit_Logs/` folder and appends every run to a chronological master log for compliance verification.
* **Salted HMAC-SHA256:** High-security deterministic hashing that maintains referential integrity for complex joins across multiple files.
* **Intelligent Auto-PII Detection:** Automated header scanning for sensitive fields (IDs, Names, Passports, DOB).
* **Flexible Output:** Supports CSV and Excel with options for format conversion and Zip archiving.
* **Architectural Rigor:** Leveraged a GenAI-assisted workflow to rapidly build a tool that is both IT-compliant and user-friendly.

## 🛠️ Installation & Build
This is a portable utility. To build the executable from source:

1. **Prerequisites:**
   ```bash
   pip install pandas openpyxl pyinstaller

Build Command
   pyinstaller --onefile --noconsole --icon=securemasker.ico --add-data "securemasker.ico;." --name Secure_Masking_Utility masker32.py


   📖 How to Use
Configure: Point the tool to your raw data folder and a secure destination.

Strategy: Choose between SHA-256 or Salted HMAC (Recommended for PII).

Select: Use "Auto-Detect PII" or manually select headers to mask.

Execute: Review the full strategy (including destination path) and run.

🗺️ Roadmap
On-Premise Web Platform: Transitioning the logic to a centralized internal portal.

GenAI Discovery: Integrating local, on-premise LLMs to allow natural language data discovery and automated masking suggestions via chat.

⚖️ License
MIT License - Developed by Shazily Munawar.


Would you like me to generate the **SHA-256 Checksum** for your final `.exe` so y
