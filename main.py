import argparse
import json
import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

def load_hosts():
    config_path = os.path.expanduser('~/.config/sshcon.json')
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_hosts(hosts):
    config_path = os.path.expanduser('~/.config/sshcon.json')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as file:
        json.dump(hosts, file, indent=4)

def add_host(label, user_at_host, port=22):
    hosts = load_hosts()
    if label in hosts:
        print(f"Host with label '{label}' already exists. Please use a unique label.")
        return

    user, host = user_at_host.split('@')
    hosts[label] = {'user': user, 'host': host, 'port': port}
    save_hosts(hosts)
    print(f"Added host '{label}' with address '{user}@{host}:{port}'.")

def delete_host(label=None):
    hosts = load_hosts()
    if not hosts:
        print("No hosts available.")
        return
    if label is None:
        host_labels = list(hosts.keys())
        host_completer = WordCompleter(host_labels, ignore_case=True, match_middle=True)
        selected_label = prompt('Select host: ', completer=host_completer)
    else:
        selected_label = label
    if selected_label in hosts:
        # Confirm deletion
        confirmation = input(f"Are you sure you want to delete {selected_label}? (y/n): ")
        if confirmation.lower() == 'y':
            del hosts[selected_label]
            save_hosts(hosts)
            print(f"Host '{selected_label}' deleted.")
        else:
            print("Deletion cancelled.")
    else:
        print("Host not found.")
def connect_to_host(label=None):
    hosts = load_hosts()
    if not hosts:
        print("No hosts available. Please add a host first.")
        return

    if label is None:
        host_labels = list(hosts.keys())
        host_completer = WordCompleter(host_labels, ignore_case=True, match_middle=True)
        selected_label = prompt('Select host: ', completer=host_completer)
    else:
        selected_label = label

    if selected_label in hosts:
        user = hosts[selected_label].get('user')
        host = hosts[selected_label].get('host')
        port = hosts[selected_label].get('port', 22)  # Default to port 22 if not specified
        connection_string = f"{user}@{host} -p {port}"

        print(f"Connecting to {connection_string}...")
        os.system(f"ssh {connection_string}")
    else:
        print("Host not found.")

# Command line parser setup
parser = argparse.ArgumentParser(description='SSH Connection Manager')
subparsers = parser.add_subparsers(dest='command')

# Add host command
add_parser = subparsers.add_parser('add', help='Add a new SSH host')
add_parser.add_argument('label', type=str, help='Label for the SSH host')
add_parser.add_argument('user_at_host', type=str, help='User and host in the format user@host')
add_parser.add_argument('port', nargs='?', default=22, type=int, help='SSH port (default: 22)')
con_parser = subparsers.add_parser('con', help='Connect to a SSH host directly')
con_parser.add_argument('label', nargs='?', type=str, help='Label for the SSH host to connect directly')
delete_parser = subparsers.add_parser('delete', help='Delete an existing SSH host')
delete_parser.add_argument('label', nargs='?', type=str, help='Label for the SSH host to delete')
args = parser.parse_args()

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        if args.command == 'add':
            add_host(args.label, args.user_at_host, args.port)
        elif args.command == 'con':
            connect_to_host(args.label)
        elif args.command == 'delete':
            delete_host(args.label)
        elif args.command is None:
            connect_to_host()
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        sys.exit(0)