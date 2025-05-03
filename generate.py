#!/usr/bin/env python3

import getpass
from passlib.hash import sha512_crypt
import sys
import os

BUILD_DIR = 'build'
USER_DATA_FILE = f"{BUILD_DIR}/user-data"
METADATA_FILE = f"{BUILD_DIR}/meta-data"

def prompt_hostname():
  hostname = input("Enter hostname (e.g. test-vm): ").strip()
  if not hostname:
    print("Hostname is required.")
    sys.exit(1)
  return hostname

def prompt_username():
  username = input("Enter username (e.g. testuser): ").strip()
  if not username:
    print("Username is required.")
    sys.exit(1)
  return username

def prompt_password():
  choice = input("Set a password? (y/N): ").strip().lower()
  if choice != 'y':
    return None
  password = getpass.getpass("Enter password: ")
  confirm = getpass.getpass("Confirm password: ")
  if password != confirm:
    print("Error: Passwords do not match.")
    sys.exit(1)
  return sha512_crypt.hash(password)

def prompt_ssh_key():
  choice = input("Provide SSH public key? (y/N): ").strip().lower()
  if choice != 'y':
    return None
  key = input("Paste your SSH public key (starts with ssh-rsa or ssh-ed25519): ").strip()
  if not key.startswith("ssh-"):
    print("Error: Invalid SSH key format.")
    sys.exit(1)
  return key

def generate_cloud_init(hostname, username, password_hash, ssh_key):
  user_block = f"""  - name: {username}
    groups: sudo
    shell: /bin/bash
    sudo: ['ALL=(ALL) NOPASSWD:ALL']"""
  if ssh_key:
    user_block += f"""
    ssh_authorized_keys:
      - {ssh_key}"""
  if password_hash:
    user_block += f"""
    passwd: '{password_hash}'"""

  return f"""#cloud-config
hostname: {hostname}
users:
{user_block}
chpasswd:
  expire: false
"""

def main():
  print("Cloud-Init user-data Generator\n")
  hostname = prompt_hostname()
  username = prompt_username()
  password_hash = prompt_password()
  ssh_key = prompt_ssh_key()

  if not password_hash and not ssh_key:
    print("Error: You must provide either a password or an SSH key.")
    sys.exit(1)

  yaml_output = generate_cloud_init(hostname, username, password_hash, ssh_key)

  if not os.path.exists(BUILD_DIR):
    os.mkdir(BUILD_DIR)
    print(f"✅ Created directory '{BUILD_DIR}'")

  with open(USER_DATA_FILE, "w") as f:
    f.write(yaml_output)
    print(f"✅ Created file '{USER_DATA_FILE}'")

  with open(METADATA_FILE, "w") as f: # Create empty file
    print(f"✅ Created file '{METADATA_FILE}'")

  with open(USER_DATA_FILE, "w") as f:
    f.write(yaml_output)

if __name__ == '__main__':
  main()
