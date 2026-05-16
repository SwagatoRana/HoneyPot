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

### Log Format Example

SSH:
```
Client 192.168.1.100 attempted login with username: admin, password: password123
192.168.1.100, admin, password123
Command b'ls' executed by 192.168.1.100
```

HTTP:
```
2026-05-16 10:30:45,123 Client with IP Address: 192.168.1.100 entered
Username: admin, Password: admin123
```

## 🛡️ Security Considerations

This is a honeypot designed to detect attacks. Use it responsibly:

- Deploy in a **controlled environment** or isolated network segment
- Do not expose to production systems
- Monitor logs regularly for attack patterns
- Use firewall rules to restrict unexpected traffic
- Consider using in conjunction with IDS/IPS systems

## 🎯 Use Cases

- **Security Research**: Understand attacker behavior and common attack vectors
- **Threat Detection**: Identify unauthorized access attempts early
- **Network Monitoring**: Detect and log suspicious SSH/HTTP activity
- **Training**: Educational purposes for cybersecurity learning
- **Incident Response**: Gather intelligence about active threats

## 📝 Example Scenarios

### Scenario 1: Monitor SSH Brute Force Attacks
```bash
python honeypy.py -a 0.0.0.0 -p 2223 -s
```
This will accept any SSH login attempt and log all credentials.

### Scenario 2: Trap WordPress Attackers
```bash
python honeypy.py -a 0.0.0.0 -p 8080 -u wordpress_admin -pw secure_password -w
```
This runs an HTTP honeypot on port 8080 that looks like WordPress login.

### Scenario 3: Selective SSH Access (Honeypot Hybrid)
```bash
python honeypy.py -a 192.168.1.100 -p 2223 -u allowed_user -pw allowed_pass -s
```
Only logs successful attempts if correct credentials are provided.

## 🔧 Customization

### Adding Custom Shell Commands

Edit `ssh_honeypot.py` in the `emulated_shell()` function to add more command responses:

```python
elif command.strip() == b'uname':
    response = b"\n" + b"Linux honeypot 5.10.0" + b"\r\n"
    creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
```

### Modifying the HTTP Login Page

Edit `templates/wp-admin.html` to customize the appearance and form fields.

## 📊 Analyzing Logs

Example Python script to analyze SSH logs:

```python
import re

with open('audits.log', 'r') as f:
    for line in f:
        if 'attempted login' in line:
            print(line.strip())
```

## ⚠️ Common Issues

### "Address already in use" Error
```
Port is already in use. Try a different port or kill the process using netstat/lsof.
```

### SSH Connection Refused
```
Ensure the firewall allows connections on the specified port.
Check that the SSH honeypot is running with: netstat -an | grep LISTEN
```

### Missing `server.key`
```
Delete the existing key file and restart - a new one will be generated automatically.
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests for:
- Additional honeypot types
- Enhanced logging capabilities
- Better command emulation
- Security improvements

## 📄 License

This project is provided as-is for educational and authorized security research purposes.

## ⚖️ Disclaimer

This tool is intended for:
- Authorized security research
- Controlled network environments
- Educational purposes

**Unauthorized access to computer systems is illegal.** Use this tool only on systems you own or have explicit permission to test.

## 🙏 Acknowledgments

Built with:
- Paramiko for SSH protocol implementation
- Flask for web framework
- Python standard library utilities

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Version**: 1.0  
**Last Updated**: May 2026  
**Status**: Active Development
