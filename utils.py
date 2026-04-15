#!/usr/bin/bash
import subprocess
import json
import os
import shutil

_OS_RELEASE = "/etc/os-release"
def detect_dist():
    data = filetodict(_OS_RELEASE)
    return data["ID"]

def filetodict(path:str):
    tmp_dict = {}

    with open(path, "r") as file:
        data = file.read().split("\n")

    for line in data:
        if line == '':
            continue
        
        if line.startswith("#"):
            continue

        tmp = line.split("=")
        _key = tmp[0]
        _value = tmp[1].replace("\"", "")

        tmp_dict[_key] = _value

    return tmp_dict

def search_binary(name: str):
    return shutil.which(name)

def execute(cmd: list, input: str = None) -> bool:
    try:
        result = subprocess.run(
            cmd,
            input=input,
            text=True,
        )
        return result.returncode == 0

    except Exception as e:
        print(e)
        return False

def enableIpForward():

    # escribir archivo
    cmd1 = [
        search_binary("sudo"),
        search_binary("tee"),
        "/etc/sysctl.d/99-wireguard.conf"
    ]

    # aplicar sysctl
    cmd2 = [
        search_binary("sudo"),
        search_binary("sysctl"),
        "--system"
    ]

    # ejecutar tee con input
    if not execute(cmd1, input="net.ipv4.ip_forward=1\n"):
        return False

    return execute(cmd2)

def buildIp(ip_range: str, host_value: int):
    def ipToInt(ip):
        a, b, c, d = map(int, ip.split("."))
        return (a << 24) | (b << 16) | (c << 8) | d

    def intToIp(n):
        return ".".join([
            str((n >> 24) & 255),
            str((n >> 16) & 255),
            str((n >> 8) & 255),
            str(n & 255)
        ])

    ip, mask = ip_range.split("/")
    mask = int(mask)

    ip_int = ipToInt(ip)

    # máscara de red
    host_bits = 32 - mask
    max_hosts = (1 << host_bits) - 1

    # validar rango
    if host_value > max_hosts:
        return None

    # IP final = red + offset
    result = ip_int + host_value

    return intToIp(result) , mask

def saveInFile(path:str, data:str):
    try:
        with open(path , "w") as file:
            file.write(data)
        return True
    
    except Exception:
        return False

if __name__ == "_1_main__":
    #filetodict key=value from
    print(
        json.dumps(
            filetodict("/etc/os-release"),
            indent=2
           )
        )

    #detect distribution
    print(
        detect_dist()
    )

    #search binarys
    print(
        json.dumps(
            search_binary("ip"),
            indent=2
        )
    )

    #execute
    print(
        execute(["ip", "addr"])
    )