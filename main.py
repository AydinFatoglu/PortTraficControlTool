import tkinter as tk
import socket

def get_local_ip():
    # Create a temporary socket
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a remote server
        temp_sock.connect(("8.8.8.8", 80))
        # Get the local IP address
        local_ip = temp_sock.getsockname()[0]
        return local_ip
    except Exception:
        return ""

def resolve_ip_address(ip_or_domain):
    try:
        ip_address = socket.gethostbyname(ip_or_domain)
        return ip_address
    except socket.gaierror:
        return ""

def check_port_traffic():
    destination = destination_entry.get()
    port_number = int(port_entry.get())
    source = source_entry.get()

    if not source:
        source = get_local_ip()
    
    # Resolve destination IP if it is a domain name
    destination_ip = resolve_ip_address(destination)
    if not destination_ip:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid destination IP or domain name.")
        return

    # Resolve source IP if it is a domain name
    source_ip = resolve_ip_address(source)
    if not source_ip:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Invalid source IP or domain name.")
        return

    protocol = protocol_var.get()

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM)

    try:
        # Bind the socket to the source IP if provided
        if source_ip:
            sock.bind((source_ip, 0))

        # Set a timeout for the connection attempt
        sock.settimeout(2)

        # Connect to the destination IP and port
        sock.connect((destination_ip, port_number))

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Port {port_number} is open to {destination_ip} using {protocol}")
    except socket.timeout:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Timeout: Port {port_number} is closed to {destination_ip} using {protocol}")
    except ConnectionRefusedError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Connection refused: Port {port_number} is closed to {destination_ip} using {protocol}")
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"An error occurred: {str(e)}")
    finally:
        # Close the socket
        sock.close()

# Create the main window
window = tk.Tk()
window.title("Segmented Network Port Traffic Check Tool")

# Set window dimensions
window_width = 480
window_height = 240

# Get screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position to center the window
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Disable window maximize button
window.resizable(False, False)

# Create and place the input fields
destination_label = tk.Label(window, text="Destination IP/Domain:")
destination_label.pack()
destination_entry = tk.Entry(window)
destination_entry.pack()

port_label = tk.Label(window, text="Port Number:")
port_label.pack()
port_entry = tk.Entry(window)
port_entry.pack()

source_label = tk.Label(window, text="Source IP/Domain (optional):")
source_label.pack()
source_entry = tk.Entry(window)
source_entry.pack()

# Auto-fill the source IP field with local IP
local_ip = get_local_ip()
if local_ip:
    source_entry.insert(tk.END, local_ip)

# Protocol selection
protocol_var = tk.StringVar()
protocol_var.set("TCP")  # Default protocol selection

protocol_frame = tk.Frame(window)
protocol_frame.pack()

protocol_label = tk.Label(protocol_frame, text="Protocol:")
protocol_label.pack(side="left")

tcp_radio = tk.Radiobutton(protocol_frame, text="TCP", variable=protocol_var, value="TCP")
tcp_radio.pack(side="left")

udp_radio = tk.Radiobutton(protocol_frame, text="UDP", variable=protocol_var, value="UDP")
udp_radio.pack(side="left")





# Create the check button
check_button = tk.Button(window, text="Check Port Traffic", command=check_port_traffic)
check_button.pack(pady=10)

# Create the result text box
result_text = tk.Text(window, height=1, width=50)
result_text.pack(pady=10)



# Start the main event loop
window.mainloop()

