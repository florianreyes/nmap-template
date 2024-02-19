#!/usr/bin/env python3

import argparse
import subprocess
from tabulate import tabulate
from datetime import datetime
import os

NMAP_TEMPLATES_FILE = input('Enter the path to the Nmap templates file: ') + '/nmap-templates.txt' if input(
    'Do you want to use a custom path for the Nmap templates file? (y/n) ') == 'y' else os.getcwd() + '/nmap-templates.txt'
PERMISSIONS = 0o644  # Permissions for the Nmap templates file


class NmapTemplate:
    def __init__(self, alias, command, created):
        self.alias = alias
        self.command = command
        self.created = created


class NmapTemplateManager:
    def __init__(self):
        self.templates = self.load_templates()

    def load_templates(self):
        if os.path.isfile(NMAP_TEMPLATES_FILE):
            with open(NMAP_TEMPLATES_FILE, 'r') as file:
                templates = {}
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        alias, command, created = parts
                        templates[alias] = NmapTemplate(
                            alias, command, created)
                return templates
        else:
            with open(NMAP_TEMPLATES_FILE, 'w'):
                pass  # Create the file if it doesn't exist
            os.chmod(NMAP_TEMPLATES_FILE, PERMISSIONS)  # Set permissions
            return {}

    def list_templates(self):
        table = []
        for alias, template in self.templates.items():
            table.append([alias, template.command, template.created])
        print(tabulate(table, headers=[
              "Alias", "Command", "Created"], tablefmt="grid"))

    def run_template(self, alias, host):
        if alias in self.templates:
            command = self.templates[alias].command.replace("<host>", host)
            subprocess.run(command, shell=True)
        else:
            print(f"Template '{alias}' not found.")

    def add_template(self, alias, command):
        if alias not in self.templates:
            with open(NMAP_TEMPLATES_FILE, 'a') as file:
                created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{alias},{command},{created}\n")
            self.templates[alias] = NmapTemplate(alias, command, created)
            print(f"Template '{alias}' added.")
        else:
            print(f"Template '{alias}' already exists.")

    def delete_template(self, alias):
        if alias in self.templates:
            del self.templates[alias]
            with open(NMAP_TEMPLATES_FILE, 'w') as file:
                for template in self.templates.values():
                    file.write(
                        f"{template.alias},{template.command},{template.created}\n")
            print(f"Template '{alias}' deleted.")
        else:
            print(f"Template '{alias}' not found.")


def main():
    parser = argparse.ArgumentParser(description="Nmap Template Tool")
    parser.add_argument("action", choices=[
                        "run", "list", "add", "delete"], help="Action to perform")
    parser.add_argument("template", nargs="?",
                        help="Template alias or command")
    parser.add_argument("command", nargs="*",
                        help="Command (if adding a template)")
    parser.add_argument("host", nargs="?", help="Target host")

    args = parser.parse_args()

    manager = NmapTemplateManager()

    if args.action == "run":
        if args.template and args.host:
            manager.run_template(args.template, args.host)
        else:
            print("Usage: nmap-t run <alias> <host>")

    elif args.action == "list":
        manager.list_templates()

    elif args.action == "add":
        if args.template and args.command:
            alias = args.template
            command = ' '.join(args.command)
            manager.add_template(alias, command)
        else:
            print("Usage: nmap-t add <alias> <command>")

    elif args.action == "delete":
        if args.template:
            manager.delete_template(args.template)
        else:
            print("Usage: nmap-t delete <alias>")


if __name__ == "__main__":
    main()
