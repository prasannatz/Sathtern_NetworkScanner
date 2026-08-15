import socket
from datetime import datetime


SERVICES = {
    20: "FTP",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
}


def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))

            if result == 0:
                return True

    except (socket.timeout, socket.error, OSError):
        pass

    return False


def generate_report(target, open_ports, start_time, end_time):
    filename = "scan_report.txt"

    with open(filename, "w", encoding="utf-8") as report:
        report.write("NETWORK PORT SCAN REPORT\n")
        report.write("=" * 40 + "\n\n")

        report.write(f"Target: {target}\n")
        report.write(
            f"Scan started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        report.write(
            f"Scan completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        duration = end_time - start_time
        report.write(f"Duration: {duration.total_seconds():.2f} seconds\n\n")

        report.write("OPEN PORTS\n")
        report.write("-" * 40 + "\n")

        if open_ports:
            for port, service in open_ports:
                report.write(
                    f"Port {port} -> {service}\n"
                )
        else:
            report.write("No open ports detected.\n")

        report.write("\n")
        report.write(f"Total open ports: {len(open_ports)}\n")

    return filename


def main():
    target = input("Enter target (IP or domain): ").strip()

    if not target:
        print("Error: Target cannot be empty.")
        return

    print(f"\nScanning {target}...\n")

    try:
        target_ip = socket.gethostbyname(target)
        print(f"Resolved IP: {target_ip}\n")
    except socket.gaierror:
        print("Error: Could not resolve the target.")
        return

    start_time = datetime.now()
    open_ports = []

    # Scan ports 1-200
    for port in range(1, 201):
        if scan_port(target_ip, port):
            service = SERVICES.get(port, "Unknown")
            open_ports.append((port, service))
            print(f"[OPEN] Port {port} -> {service}")

    end_time = datetime.now()

    report_file = generate_report(
        target,
        open_ports,
        start_time,
        end_time
    )

    print("\nScan completed.")
    print(f"Open ports found: {len(open_ports)}")
    print(f"Scan report saved as: {report_file}")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()