import os
import time
import socket
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
import ping3
import requests

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_valid_ipv4_address(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False

def check_tcp(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.1)
        try:
            sock.connect((host, port))
            return "ONLINE"
        except (socket.timeout, socket.error):
            return "OFFLINE"

def check_udp(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(0.1)
        try:
            sock.sendto(b"", (host, port))
            data, addr = sock.recvfrom(1024)
            return "ONLINE"
        except (socket.timeout, socket.error):
            return "OFFLINE"

def check_icmp(host):
    if is_valid_ipv4_address(host):
        response = ping3.ping(host, timeout=0.1)
        if response is not None:
            return "ONLINE"
        else:
            return "OFFLINE"
    else:
        return "INVALID HOST"

def print_status(host, port, protocol, status):
    user_name = os.getlogin()
    watermark = Text("[+] Made by Stragar", style="bold white")
    if status == "ONLINE":
        status_text = Text()
        status_text.append("root", style="bold white")
        status_text.append(f"@{user_name}", style="bold red")
        status_text.append(": ", style="bold white")
        status_text.append("CONNECTED ", style=Style(color="white", bgcolor="green"))
        status_text.append(" to ", style="bold white")
        status_text.append("[", style="bold white")
        status_text.append(f"{host}:{port}", style="bold green")
        status_text.append("] ", style="bold white")
        status_text.append("[", style="bold white")
        status_text.append("+", style="bold green")
        status_text.append("] Status : ", style="bold white")
        status_text.append("ONLINE", style=Style(color="white", bgcolor="green"))
    elif status == "OFFLINE":
        status_text = Text()
        status_text.append("root", style="bold white")
        status_text.append(f"@{user_name}", style="bold red")
        status_text.append(": ", style="bold white")
        status_text.append("DOWNED", style=Style(color="white", bgcolor="red"))
        status_text.append("[", style="bold white")
        status_text.append(f"{host}:{port}", style="bold red")
        status_text.append("] ", style="bold white")
        status_text.append("[", style="bold white")
        status_text.append("-", style="bold red")
        status_text.append("] Status : ", style="bold white")
        status_text.append("OFFLINE", style=Style(color="white", bgcolor="red"))
    else:
        status_text = Text()
        status_text.append("root", style="bold white")
        status_text.append(f"@{user_name}", style="bold red")
        status_text.append(": ", style="bold white")
        status_text.append("INVALID HOST ", style=Style(color="white", bgcolor="yellow"))
        status_text.append("[", style="bold white")
        status_text.append(f"{host}", style="bold yellow")
        status_text.append("] ", style="bold white")
        status_text.append("[", style="bold white")
        status_text.append("!", style="bold yellow")
        status_text.append("] Status : ", style="bold white")
        status_text.append("INVALID HOST", style=Style(color="white", bgcolor="yellow"))
    status_text.append("\n")
    status_text.append(watermark)
    console.print(Panel(status_text, style="on black"))

def ip_info():
    clear_screen()
    ip_address = input("Enter IP address: ")
    if not is_valid_ipv4_address(ip_address):
        console.print(Text("Invalid IP address.", style="bold red"))
        time.sleep(2)
        return

    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)
    if response.status_code == 200:
        ip_data = response.json()
        ip_info_text = Text("\n[+] IP :\n", style="bold magenta")
        ip_info_text.append(f"IP Address: {ip_data.get('ip')}\n", style="cyan")
        ip_info_text.append(f"Hostname: {ip_data.get('hostname')}\n", style="cyan")
        ip_info_text.append(f"City: {ip_data.get('city')}\n", style="cyan")
        ip_info_text.append(f"Region: {ip_data.get('region')}\n", style="cyan")
        ip_info_text.append(f"Country: {ip_data.get('country')}\n", style="cyan")
        ip_info_text.append(f"Location: {ip_data.get('loc')}\n", style="cyan")
        ip_info_text.append(f"Organization: {ip_data.get('org')}\n", style="cyan")
        console.print(ip_info_text)
    else:
        console.print(Text("Could not retrieve information.", style="bold red"))
    
    time.sleep(10)
    clear_screen()

def check_for_updates():
    console.print(Text("Checking for updates...", style="bold blue"))
    time.sleep(1)
    update_url = "https://raw.githubusercontent.com/StraGar0/pinger/main/main.py"
    local_file = __file__
    
    response = requests.get(update_url)
    if response.status_code == 200:
        remote_code = response.text
        with open(local_file, 'r') as file:
            local_code = file.read()
        if local_code != remote_code:
            with open(local_file, 'w') as file:
                file.write(remote_code)
            console.print(Text("Update found and applied. Please restart the program.", style="bold green"))
            time.sleep(5)
            exit()
        else:
            console.print(Text("No updates found. You have the latest version.", style="bold green"))
            time.sleep(2)
    else:
        console.print(Text("Could not check for updates.", style="bold red"))
        time.sleep(2)

def main():
    check_for_updates()
    while True:
        clear_screen()
        title = Text("TOOLS", style="bold blue on black", justify="center")
        subtitle = Text("🔧 DEV STRAGAR ", style="bold magenta on black", justify="center")
        
        console.print(Panel(title, style="on black"))
        console.print(Panel(subtitle, style="on black"))

        main_menu = Text("Main Menu:\n", style="bold magenta")
        main_menu.append("1. IP Info\n", style="cyan")
        main_menu.append("2. Pinger\n", style="cyan")
        console.print(main_menu)

        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            ip_info()
        elif choice == "2":
            ping_menu()
        else:
            console.print(Text("Invalid choice.", style="bold red"))
            time.sleep(2)

def ping_menu():
    clear_screen()
    ping_menu_text = Text("Ping Menu:\n", style="bold magenta")
    ping_menu_text.append("1. TCP\n", style="cyan")
    ping_menu_text.append("2. UDP\n", style="cyan")
    ping_menu_text.append("3. ICMP\n", style="cyan")
    console.print(ping_menu_text)
    
    method_choice = input("Enter your choice (1/2/3): ")
    if method_choice == "1":
        clear_screen()
        host = input("Enter IP address: ")
        port = int(input("Enter port: "))
        while True:
            tcp_status = check_tcp(host, port)
            console.print("\n[+] TCP Status:")
            print_status(host, port, "TCP", tcp_status)
            time.sleep(1)
    elif method_choice == "2":
        clear_screen()
        host = input("Enter IP address: ")
        port = int(input("Enter port: "))
        while True:
            udp_status = check_udp(host, port)
            console.print("\n[+] UDP Status:")
            print_status(host, port, "UDP", udp_status)
            time.sleep(1)
    elif method_choice == "3":
        clear_screen()
        host = input("Enter IP address: ")
        while True:
            icmp_status = check_icmp(host)
            console.print("\n[+] ICMP Status:")
            print_status(host, None, "ICMP", icmp_status)
            time.sleep(1)
    else:
        console.print(Text("Invalid choice.", style="bold red"))
        time.sleep(2)
        clear_screen()
        ping_menu()

if __name__ == "__main__":
    main()
