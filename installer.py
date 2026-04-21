#!/user/bin/bash
import os
import sys

from modules.package_installer import package_installer, detect_dist, remove_package
from modules.utils import enableIpForward, filetodict, buildIp, saveInFile, execute
from vars.distribution_packages import dist_packages
from vars.vars import required_keys
from modules.genCredentials import genCredentials
from modules.wg_fun import enableWireguard , upWireguard, install_wg
from vars.paths import wg_root , settings_path

def server_settings(settings_path:str):
    loadSettings = filetodict(settings_path)

    for key ,  value in loadSettings.items():
        if value == "":
            print(f"  [-] Setting '{key}' has to have a value.")
            return False

    return loadSettings

def installer():
    print("[!] Wireguard installer")
    print(f"  Detected distribution: " , detect_dist())


    print("[!] Installing packages")
    install_wg()


    print("[!] Enabling ip forward")
    if enableIpForward():
        print("  [+] Enabled successfully.")
    else:
        print("  [-] Not enabled.")
        sys.exit(1)


    print("[!] Loading config.")
    #setup settings
    if os.path.exists(settings_path) == False:
        print("[!] Fatal error 'settings' file is required.")
        sys.exit(1)
    
    config = server_settings(settings_path)
    if type(config) == bool:
        sys.exit(1)

    for _key in config:
        if not _key in required_keys:
            print(f"  [-] Key {_key} not recognized.")
            sys.exit(1)

    print(f"[!] Verify if {wg_root} exists.")
    #create /etc/wireguard
    if not os.path.exists(wg_root):
        cmd = ["sudo" , "mkdir" , wg_root]
        if execute(cmd):
            print(f"  [*] {wg_root} was created.")
        else:
            print(f"  [*] {wg_root} was not created.")

    print("[!] Setting up server")
    #create wg0.conf
    credentials_path = os.path.join(os.path.join(wg_root), "credentials")
    if not os.path.exists(credentials_path):
        cmd = ["sudo" , "mkdir" , credentials_path]
        execute(cmd)
    
    server_credentials_path = os.path.join(credentials_path, "server") 

    if not os.path.exists(server_credentials_path):
        cmd = ["sudo", "mkdir" , server_credentials_path]
        execute(cmd)

    server_privkey , server_pubkey = genCredentials()

    if saveInFile(
        os.path.join(server_credentials_path, "privkey"),
        server_privkey
    ):
        print("  [+] Server private key generated successfully.")
    else:
        print("  [-] Server private key not generated.")

    if saveInFile(
        os.path.join(server_credentials_path, "pubkey"),
        server_pubkey
    ):
        print("  [+] Server public key generated successfully.")
    else:
        print("  [-] Server public key not generated.")


    server_ip, mask = buildIp(config["ip_range"], 1)    
    listen_port = config["listen_port"]
    dns = config["dns"]
    post_up = config["post_up"]
    post_down = config["post_down"]

    server_wg0_content = [
         "[Interface]",
        f"Address = {server_ip}",
        f"PrivateKey = {server_privkey}",
        f"ListenPort = {listen_port}",
        f"DNS = {dns}",
        f"PostUp = {post_up}",
        f"PostDown = {post_down}"
    ]

    #generate clients configuration
    print(" [!] Setting up peers")
    peers = config["peers"]
    if not peers.isdigit():
        print("[-] Setting peers must be a digit.")
        sys.exit(1)
    peers = int(peers)

    for _index in range(1 , peers + 1):
        peer_privkey , peer_pubkey = genCredentials()
    
        peer_credentials_path = os.path.join(credentials_path, f"peer{_index}") 
        if not os.path.exists(peer_credentials_path):
            cmd = ["sudo" , "mkdir", peer_credentials_path]
            if execute(cmd):
                print(f"  [*] {peer_credentials_path} was created.")
            else:
                print(f"  [*] {peer_credentials_path} was not created.")


        if saveInFile(
            os.path.join(peer_credentials_path, "privkey"),
            peer_privkey
        ):
            print(f"   [+] Peer{_index} private key generated successfully.")
        else:
            print(f"   [-] Peer{_index} private key not generated.")

        if saveInFile(
            os.path.join(peer_credentials_path, "pubkey"),
            peer_pubkey
        ):
            print(f"   [+] Peer{_index} public key generated successfully.")
        else:
            print(f"   [-] Peer{_index} public key not generated.")

        peer_ip , mask = buildIp(config["ip_range"], _index + 1)
        remote_ip = config["remote_ip"]
        allow_ips = config["allow_ips"]
        keep_alive = config["keep_alive"]

        client_wg0_content = [
             "[Interface]",
            f"PrivateKey = {peer_privkey}",
            f"Address = {peer_ip}/32",
            "",
            f"[Peer]",
            f"PublicKey = {server_pubkey}",
            f"Endpoint = {remote_ip}:{listen_port}",
            f"AllowedIPs = {allow_ips}",
            f"PersistentKeepalive  = {keep_alive}"
        ]

        add_peer_in_server_wg0_content = [
            "",
            f"#peer{_index}",
            "[Peer]",
            f"PublicKey = {peer_pubkey}",
            f"AllowedIPs = {peer_ip}/32"
        ]

        if saveInFile(
            os.path.join(peer_credentials_path, "wg0.conf"),
            "\n".join(client_wg0_content)
            ):
            print("   [*] Peer 'wg0.conf' saved successfully.")
        else:
            print("   [*] Peer 'wg0.conf' not saved.")

        #agrega el peer a la configuracion del server
        server_wg0_content.extend(add_peer_in_server_wg0_content)
    
    if saveInFile(
        os.path.join(wg_root, "wg0.conf"),
        "\n".join(server_wg0_content)
        ):
        print("  [*] Server 'wg0.conf' saved successfully.")
    else:
        print("  [*] Server 'wg0.conf' not saved.")
    
    enableWireguard()
    upWireguard()