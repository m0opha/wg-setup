#!/usr/bin/bash

from utils import search_binary , execute

def downWireguard():
    print("[*] Bringing down interface wg0...")
    cmd = ["sudo", "wg-quick", "down", "wg0"]
    
    if not execute(cmd):
        print("[!] Failed to bring down wg0:")
        return False

    print("[+] Interface wg0 successfully brought down.")
    return True

def upWireguard():
    cmd = ["sudo", "wg-quick", "up", "wg0"]

    if not execute(cmd):
        print("[!] Error bringing up wg0:")
        return False

    print("[+] Interface wg0 successfully brought up.")
    return True

def enableWireguard():
    print("[*] Enabling automatic startup with systemd...")

    cmd1 = ["sudo", "systemctl", "enable", "wg-quick@wg0"]
    cmd2 = ["sudo", "wg-quick", "down", "wg0"]
    if not execute(cmd1):
        print("[!] Failed to enable service:")

        if execute(cmd2):
            print("[+] Interface wg0 successfully brought down.")

        return False

    print("[+] wg-quick@wg0 service enabled successfully.")
    return True