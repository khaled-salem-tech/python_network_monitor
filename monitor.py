import socket
from datetime import datetime
import ipaddress





def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.create_connection((host, port), timeout=timeout)
        return True
    except OSError:
        return False

def get_network_info():
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except OSError:
        ip = "Unknown"
    finally:
        s.close()
    return hostname, ip

def check_port(host, port,timeout=1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    result = s.connect_ex((host, port))
    s.close()
    return result == 0

def log(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("monitor.log","a") as f:
        f.write(f"[{time}] {message}\n")

def is_private_ip(host):
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return False


def scan_ports(host):
    ports = input("Ports (e.g. 80,443,445): ")
    for p in ports.split(","):
        try:
            p = int(p.strip())
        except ValueError:
            print("Invalid port:", p)
            continue
        status = "open" if check_port(host, p) else "closed"
        print(p, status)
        log(f"Port {p} on {host}: {status}")

def main():
    print("1) Check internet")
    print("2) Network info")
    print("3) Check ports on this device")
    print("4) Check ports on another device")
    choice = input("Choose: ")

    if choice == "1":
        status = check_internet()
        print("Internet:", "connected" if status else "not connected")
        log(f"Internet check: {status}")
    elif choice == "2":
        hostname, ip = get_network_info()
        print("Hostname:", hostname)
        print("IP:", ip)
        log(f"Network info: {hostname}, {ip}")
    elif choice == "3":
        scan_ports("127.0.0.1")
    elif choice == "4":
        host = input("Target IP or hostname: ").strip()
        if not host:
            print("No target entered.")
            return
        if not is_private_ip(host):
            answer = input("This target is outside your local network. "
                           "Do you own it or have permission to scan it? (yes/no): ")
            if answer.strip().lower() != "yes":
                print("Cancelled.")
                return
            log(f"Permission confirmed for external target {host}")
        scan_ports(host)
    else:
        print("Invalid option")


main()
