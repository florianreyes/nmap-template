# Nmap Template Tool (nt)

A simple command-line tool to create, execute, manage, and delete Nmap scan templates. This tool allows you to store commonly used Nmap commands and run them with a single command, making your scanning process faster and more efficient.

---

### Features

- **Create** custom Nmap scan templates.
- **Execute** saved templates with IP address substitution.
- **List** all saved templates in a beautiful table format.
- **Delete** templates that are no longer needed.

---

### Requirements

- Python 3.x
- Nmap
- A terminal

---

### Installation

1. Clone the repository or download the script:
   ```bash
   git clone https://github.com/yourusername/nmap-template-tool.git
   ```
2. Make executable:
  ```bash
cd nmap-template-tool
chmod +x nt
```
3. Move to PATH

### Example Usage

```bash
nt create scan1 "nmap -sS -p 22,80 <ip>"
```
```bash
nt exec scan1 192.168.1.1
```
