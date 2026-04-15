#!/usr/bin/bash
import subprocess

from utils import execute, search_binary

def genCredentials():
    cmd1 = [search_binary("wg"), "genkey"]
    cmd2 = [search_binary("wg"), "pubkey"]

    privatekey = subprocess.run(
        cmd1,
        capture_output=True,
        text=True
        ).stdout.strip()
    
    publickey = subprocess.run(
        cmd2,
        input=privatekey,
        capture_output=True,
        text=True
    ).stdout.strip()
       
    return privatekey , publickey

if __name__ == "__main__":
    privatekey , publickey = genCredentials()
    print(f"Private key: {privatekey}")
    print(f"Public key: {publickey}")