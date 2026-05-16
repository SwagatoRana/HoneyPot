# HoneyPy - A Deceptive Honeypot Framework

A Python-based honeypot framework that simulates vulnerable services to detect and log unauthorized access attempts. HoneyPy supports both SSH and HTTP honeypots with detailed logging capabilities.

## 📋 Features

- **SSH Honeypot**: Emulates a fake SSH server with customizable credentials
  - Logs all connection attempts with IP addresses
  - Records login attempts and their credentials
  - Emulates basic shell commands (pwd, whoami, ls, cat, exit)
  - Rotates log files automatically
  - Generates RSA key pairs automatically on first run

- **HTTP Honeypot**: Simulates a WordPress admin login page
  - Renders realistic WordPress login interface
  - Logs all login attempts with timestamps and source IPs
  - Tracks attempted credentials
  - Customizable username/password for testing

- **Flexible Configuration**: Support for custom ports, hostnames, and credentials
- **Comprehensive Logging**: Separate audit logs for different honeypot types
- **Multi-threaded**: Handles multiple concurrent connections

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HoneyPy.git
cd HoneyPy
```

2. Install dependencies:
```bash
pip install paramiko flask
```

### Dependencies

- **paramiko**: SSH protocol implementation for the SSH honeypot
- **flask**: Web framework for the HTTP honeypot

## 📖 Usage

### Running the SSH Honeypot

```bash
# Allow any credentials
python honeypy.py -a 0.0.0.0 -p 2223 -s

# Require specific credentials
python honeypy.py -a 0.0.0.0 -p 2223 -u admin -pw secretpass -s
```

### Running the HTTP Honeypot

```bash
# Use default credentials (admin/password)
python honeypy.py -a 0.0.0.0 -p 5000 -w

# Use custom credentials
python honeypy.py -a 0.0.0.0 -p 5000 -u administrator -pw mypassword -w
```

### Command-Line Arguments

| Argument | Short | Type | Required | Description |
|----------|-------|------|----------|-------------|
| `--address` | `-a` | string | Yes | Bind address (e.g., 0.0.0.0 or localhost) |
| `--port` | `-p` | integer | Yes | Port to listen on |
| `--username` | `-u` | string | No | Username for authentication (SSH/HTTP) |
| `--password` | `-pw` | string | No | Password for authentication (SSH/HTTP) |
| `--ssh` | `-s` | flag | No | Run SSH honeypot |
| `--http` | `-w` | flag | No | Run HTTP honeypot |

## 📁 Project Structure

```
HoneyPy/
├── honeypy.py              # Main entry point and CLI handler
├── ssh_honeypot.py         # SSH honeypot implementation
├── web_honeypot.py         # HTTP/Flask honeypot implementation
├── server.key              # SSH RSA private key (auto-generated)
├── server.key.pub          # SSH RSA public key
├── templates/
│   └── wp-admin.html       # WordPress login page template
├── audits.log              # SSH connection/audit logs
├── cmd_audits.log          # SSH command execution logs
└── http_audits.log         # HTTP login attempt logs
```

## 🔍 Logging

### SSH Honeypot Logs

- **audits.log**: Connection attempts, login credentials, and connection details
- **cmd_audits.log**: Emulated shell commands executed by attackers

### HTTP Honeypot Logs

- **http_audits.log**: Login attempts with timestamps, source IPs, and attempted credentials

All logs use rotating file handlers with a 2KB size limit and keep up to 5 backup files.

## ⚖️ Disclaimer

This tool is intended for:
- Security research
- Controlled network environments
- Educational purposes

**Unauthorized access to computer systems is illegal.** Use this tool only on systems you own or have explicit permission to test.

Built with:
- Paramiko for SSH protocol implementation
- Flask for web framework
- Python standard library utilities
