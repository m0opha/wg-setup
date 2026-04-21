#!/usr/bin/bash

from modules.utils import search_binary , execute, detect_dist
from modules.package_installer import package_installer, remove_package
from vars.distribution_packages import dist_packages

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


def install_wg():
    distribution = detect_dist()
    supported_dist = list(dist_packages.keys())
    
    if not distribution in supported_dist:
        print("[!] Distribution not supported.")
        return 
    
    for _package in dist_packages[distribution]:
        if package_installer(_package, distribution):
            print(f"    [+] {_package} installed successfully.")
        else:
            print(f"    [-] {_package} Not installed.")
            

def remove_wg():
    distribution = detect_dist()
    supported_dist = list(dist_packages.keys())
    
    if not distribution in supported_dist:
        print("[!] Distribution not supported.")
        return 
    
    for _package in dist_packages[distribution]:
        if remove_package(_package, distribution):
            print(f"  [+] {_package} removed successfully.")
        else:
            print(f"  [-] {_package} Not removed.")
            