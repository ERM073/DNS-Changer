import tkinter as tk
from tkinter import ttk
import subprocess
import psutil

def get_network_interfaces():
    interfaces = []
    for interface, addrs in psutil.net_if_addrs().items():
        interfaces.append(interface)
    return interfaces

def change_dns():
    selected_interface = interface_combobox.get()
    selected_dns = dns_servers.get(dns_listbox.get(tk.ACTIVE))  # Get selected DNS server

    primary_dns = selected_dns[0]
    secondary_dns = selected_dns[1]

    cmd_primary = f'netsh interface ipv4 set dns name="{selected_interface}" static {primary_dns} primary'
    cmd_secondary = f'netsh interface ipv4 add dnsservers name="{selected_interface}" address={secondary_dns} index=2'

    try:
        subprocess.run(cmd_primary, shell=True, check=True)
        subprocess.run(cmd_secondary, shell=True, check=True)
        result_label.config(text=f"DNS settings changed to primary: {primary_dns}, secondary: {secondary_dns}.")
    except subprocess.CalledProcessError:
        result_label.config(text="Error changing DNS settings.")

# Create the main window
root = tk.Tk()
root.title("DNS Changer")

# Apply a style to ttk widgets
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="#007acc", foreground="white")
style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
style.configure("TListbox", background="white", font=("Helvetica", 12))

# Get a list of network interfaces
interfaces = get_network_interfaces()

# Create a label for network interface selection
label_interface = ttk.Label(root, text="Select a network interface:")
label_interface.pack(pady=10, padx=20, anchor="w")

# Create a combo box to select a network interface
interface_combobox = ttk.Combobox(root, values=interfaces)
interface_combobox.set(interfaces[0])  # Set the default interface
interface_combobox.pack(pady=5, padx=20, fill="x")

# Create a label for DNS server selection
label_dns = ttk.Label(root, text="Select a DNS server:")
label_dns.pack(pady=10, padx=20, anchor="w")

# Dictionary of DNS servers and their corresponding addresses
dns_servers = {
    "Google": ["8.8.8.8", "8.8.4.4"],
    "CloudFlare": ["1.1.1.1", "1.0.0.1"],
    "OpenDNS": ["208.67.222.222", "208.67.220.220"],
    "AdGuard": ["94.140.14.14", "94.140.15."],
}  # Add more DNS servers if needed

# Create a listbox to display DNS server options
dns_listbox = tk.Listbox(root)
for server in dns_servers.keys():
    dns_listbox.insert(tk.END, server)
dns_listbox.pack(pady=5, padx=20, fill="x")

# Create a button to change DNS
change_button = ttk.Button(root, text="Change DNS", command=change_dns)
change_button.pack(pady=10, padx=20, fill="x")

# Create a label to display the result
result_label = ttk.Label(root, text="")
result_label.pack(pady=10, padx=20, anchor="w")

# Start the Tkinter main loop
root.mainloop()
