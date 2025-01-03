import json
import subprocess
import yaml
import os

def get_terraform_output():
    """Get Terraform output in JSON format"""
    try:
        result = subprocess.run(
            ['terraform', 'output', '-json'],
            capture_output=True,
            text=True,
            check=True,
            cwd='terraform'
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error getting Terraform output: {e}")
        return None

def generate_inventory(tf_output):
    """Generate Ansible inventory from Terraform output"""
    inventory = {
        'all': {
            'hosts': {
                'vpn_server': {
                    'ansible_host': tf_output['vpn_public_ip']['value'],
                    'ansible_user': 'ubuntu',
                    'ansible_ssh_private_key_file': '~/.ssh/vpn-key'
                }
            }
        }
    }
    return inventory

def save_inventory(inventory):
    """Save inventory to YAML file"""
    os.makedirs('ansible/inventory', exist_ok=True)
    inventory_path = 'ansible/inventory/hosts.yml'
    
    with open(inventory_path, 'w') as f:
        yaml.dump(inventory, f, default_flow_style=False)
    
    print(f"Inventory file generated at: {inventory_path}")

def main():
    tf_output = get_terraform_output()
    if tf_output:
        inventory = generate_inventory(tf_output)
        save_inventory(inventory)

if __name__ == '__main__':
    main()