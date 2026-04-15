#!/usr/bin/bash


from utils import detect_dist, search_binary, execute

def package_installer(package:str, distribution:str):

    if distribution == "debian" or distribution == "ubuntu":
        cmd = [search_binary("sudo"),search_binary("apt"), "install", "-y", "-qq", package]
           
    elif distribution == "amzn" or distribution == "fedora":
        cmd = [search_binary("sudo") , search_binary("dnf") , "install", "-y", "-q" , package]
    
    else:
        print("[!] Distribution not suported.")
        return False
    
    return execute(cmd)

def remove_package(package:str, distribution):

    if distribution == "debian" or distribution == "ubuntu":
        cmd = [search_binary("sudo"),search_binary("apt"), "remove", "-y", "-qq", package]
           
    elif distribution == "amzn" or distribution == "fedora":
        cmd = [search_binary("sudo") , search_binary("dnf") , "remove", "-y", "-q" , package]
    
    else:
        print("[!] Distribution not suported.")
        return False
    
    return execute(cmd)