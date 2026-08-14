import socket

services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
}

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)   
        result = s.connect_ex((target, port))
        s.close()

        if result == 0:
            return True
        else:
            return False

    except:
        return False


def main():
    target = input("Enter target (IP or domain): ")

    print(f"\nScanning {target}...\n")

   
    for port in range(1, 201):
        print(f"Scanning port {port}...", end="\r")

        if scan_port(target, port):
            service = services.get(port, "Unknown")
            print(f"[OPEN] Port {port} -> {service}")

    print("\nScan completed.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()