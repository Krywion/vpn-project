import os
import sys
import subprocess
import json
from typing import Optional
from pathlib import Path
import socket
import time

class VPNManager:
    def __init__(self):
        self.regions = {
            "us-east-1": "N. Virginia",
            "us-east-2": "Ohio",
            "us-west-1": "N. California",
            "us-west-2": "Oregon",
            "eu-west-1": "Ireland",
            "eu-west-2": "London",
            "eu-west-3": "Paris",
            "eu-central-1": "Frankfurt",
            "ap-northeast-1": "Tokyo",
            "ap-northeast-2": "Seoul",
            "ap-southeast-1": "Singapore",
            "ap-southeast-2": "Sydney",
            "ap-south-1": "Mumbai",
            "sa-east-1": "São Paulo"
        }
        self.config_dir = Path.home() / '.vpn-client'
        self.terraform_dir = Path(__file__).parent.parent / 'terraform'
        self.ansible_dir = Path(__file__).parent.parent / 'ansible'
        
    def init_directories(self):
        self.config_dir.mkdir(exist_ok=True)
        
    def validate_region(self, region: str) -> bool:
        return region in self.regions

    def wait_for_ssh(self, server_ip: str, timeout: int = 180, interval: int = 10):
        print("Waiting for server to be ready...")
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for server to be ready")
                
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((server_ip, 22))
                sock.close()
                
                if result == 0:
                    time.sleep(2)
                    print("Server is ready")
                    return True
                    
            except socket.error:
                pass
                
            print(f"Server is not ready yet, waiting {interval} seconds...")
            time.sleep(interval)

    def init_server_config(self, region: str):
        if not self.validate_region(region):
            print(f"Error: Invalid region '{region}'")
            return False
            
        try:
            # Terraform configuration
            os.environ['AWS_REGION'] = region
            terraform_commands = [
                ['terraform', 'init'],
                ['terraform', 'plan', '-var', f'aws_region={region}'],
                ['terraform', 'apply', '-auto-approve', '-var', f'aws_region={region}']
            ]
            
            for cmd in terraform_commands:
                subprocess.run(cmd, cwd=self.terraform_dir, check=True)
                
            result = subprocess.run(
                ['terraform', 'output', '-json'],
                cwd=self.terraform_dir,
                capture_output=True,
                text=True,
                check=True
            )
            
            outputs = json.loads(result.stdout)
            server_ip = outputs['vpn_public_ip']['value']
            
            self.wait_for_ssh(server_ip)
            self.update_ansible_inventory(server_ip)
            
            # Ansible configuration
            subprocess.run(
                ['ansible-playbook', '-i', 'inventory/hosts.yml', 'playbooks/main.yml'],
                cwd=self.ansible_dir,
                check=True
            )
            
            print(f"Server VPN was successfully configured in {self.regions[region]}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error during server configuration: {str(e)}")
            return False

    def terminate_server(self, region: str):
        if not self.validate_region(region):
            print(f"Error: Invalid region '{region}'")
            return False
            
        try:
            os.environ['AWS_REGION'] = region
            subprocess.run(
                ['terraform', 'destroy', '-auto-approve', '-var', f'aws_region={region}'],
                cwd=self.terraform_dir,
                check=True
            )
            print(f"VPN server in {self.regions[region]} was successfully terminated")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error during server termination: {str(e)}")
            return False 

    def update_ansible_inventory(self, server_ip: str):
        inventory_content = f"""all:
  hosts:
    vpn_server:
      ansible_host: "{server_ip}"
      ansible_user: ubuntu
      ansible_ssh_private_key_file: "~/.ssh/vpn-key"
"""
        inventory_file = self.ansible_dir / 'inventory/hosts.yml'
        inventory_file.write_text(inventory_content)
        
    def connect(self):
        config_file = Path.home() / 'client1.ovpn'
        if not config_file.exists():
            print("Error: VPN configuration file not found")
            return False
            
        try:
            subprocess.run(['sudo', 'openvpn', '--config', str(config_file)], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to VPN server: {str(e)}")
            return False
            
    def disconnect(self):
        try:
            subprocess.run(['sudo', 'killall', 'openvpn'], check=True)
            print("Disconnected from VPN server")
            return True
        except subprocess.CalledProcessError:
            print("Error disconnecting from VPN server")
            return False
            
    def list_servers(self):
        print("Available VPN servers:")
        for i, (region, name) in enumerate(self.regions.items(), 1):
            print(f" {i}. {region} ({name})")

def main():
    if len(sys.argv) < 2:
        print("Error: No option provided")
        print("Use 'vpn-connect.py --help' to see available options")
        return
        
    vpn = VPNManager()
    option = sys.argv[1]
    
    if option in ['-h', '--help']:
        print("Usage: vpn-connect.py [OPTION]")
        print("Options:")
        print("  -h, --help                      View help information")
        print("  -l, --list                      View available VPN servers")
        print("  -c, --connect                   Connect to VPN server")
        print("  -d, --disconnect                Disconnect from VPN server")
        print("  -s REGION, --server REGION      Initialize VPN server in specified region")
        print("  -k REGION, --kill REGION        Terminate VPN server in specified region")
        
    elif option in ['-l', '--list']:
        vpn.list_servers()
        
    elif option in ['-c', '--connect']:
        vpn.connect()
        
    elif option in ['-d', '--disconnect']:
        vpn.disconnect()
        
    elif option in ['-s', '--server']:
        if len(sys.argv) < 3:
            print("Error: No region provided")
            print("Use 'vpn-connect.py --list' to see available regions")
            return
        vpn.init_server_config(sys.argv[2])

    elif option in ['-k', '--kill']:
        if len(sys.argv) < 3:
            print("Error: No region provided")
            print("Use 'vpn-connect.py --list' to see available regions")
            return
        vpn.terminate_server(sys.argv[2])
        
    else:
        print(f"Error: Invalid option: '{option}'")
        print("Use 'vpn-connect.py --help' to see available options")

if __name__ == "__main__":
    main()