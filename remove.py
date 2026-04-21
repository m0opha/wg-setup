#!/usr/bin/bash
import os

from modules.wg_fun import remove_wg
from vars.paths import wg_root
from modules.utils import detect_dist, execute

def remove():
    print("[!] Wireguard remover.")
    print("  Distribution detected: " ,detect_dist())
    remove_wg()

    if os.path.exists(wg_root):
        print(f"[!] Removing {wg_root}")
        cmd = ["sudo" , "rm" , "-rf" , wg_root]
        
        if execute(cmd):
            print(f"  [*] {wg_root} was created.")
        else:
            print(f"  [*] {wg_root} was not created.")