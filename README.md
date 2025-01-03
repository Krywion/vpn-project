# Personal VPN Server Infrastructure
### 🌐 Overview
This project provides an automated solution for deploying and managing personal VPN servers across multiple AWS regions. It combines infrastructure as code (Terraform), configuration management (Ansible), and a convenient Python CLI tool for seamless management.
### 🚀 Features

* Multi-Region Support: Deploy VPN servers in 14 different AWS regions
* Automated Deployment: One-command deployment using Terraform
* Secure Configuration: Hardened server setup with OpenVPN, fail2ban, and UFW
* Easy Management: Simple CLI tool for deployment, connection, and termination
* Infrastructure as Code: Full AWS infrastructure defined in Terraform
* Automated Configuration: Ansible playbooks for consistent server setup

### 🛠 Technology Stack

* Infrastructure: Terraform
* Configuration Management: Ansible
* VPN Software: OpenVPN
* Cloud Provider: AWS
* Programming Language: Python
* Security: UFW, fail2ban

### 📋 Prerequisites

* AWS Account and configured AWS CLI
* Terraform installed
* Ansible installed
* Python 3.x
* OpenVPN client

### 🔧 Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/vpn-project.git
cd vpn-project
```

2. Generate SSH key pair
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/vpn-key
```

3. Configure AWS credentials
```bash
aws configure
```

### 💻 Usage
The project includes a CLI tool (vpn-connect.py) for managing VPN servers:

```bash
# List available regions
python3 vpn-connect.py --list

# Deploy VPN server in a region
python3 vpn-connect.py --server eu-central-1

# Connect to VPN
python3 vpn-connect.py --connect

# Disconnect from VPN
python3 vpn-connect.py --disconnect

# Terminate VPN server
python3 vpn-connect.py --kill eu-central-1
```

### 📁 Project Structure

```
.
├── ansible/
│   ├── playbooks/
│   ├── roles/
│   └── inventory/
├── terraform/
│   ├── main.tf
│   ├── vpc.tf
│   └── ...
├── scripts/
│   └── vpn-connect.py
└── README.md
```

### 🔐 Security Features

* SSH hardening with key-based authentication
* fail2ban for brute force protection
* UFW firewall configuration
* OpenVPN with strong encryption
* Automatic security updates

### 🤝 Contributing
Feel free to submit issues, fork the repository and create pull requests for any improvements.
### 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
### ⚠️ Disclaimer
This project is for educational and personal use. Make sure to comply with AWS terms of service and your local regulations regarding VPN usage.