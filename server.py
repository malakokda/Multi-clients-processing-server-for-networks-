import socket  
import threading  
from datetime import datetime  # For time/date features and logging
HOST = '127.0.0.1'  # Server IP (localhost)
PORT = 4949  # Port number server listens on

client_counter = 0  # To assign unique names to clients
counter_lock = threading.Lock()  # prevent the race condition so no client takes the same number
log_lock = threading.Lock()  # Lock to make file logging thread-safe

def log_to_file(message):
    # Ensures only one thread writes to file at a time
    with log_lock:
        with open("server_log.txt", "a") as f:
            # Write message with timestamp
            f.write(f"{datetime.now()}: {message}\n")

def process_command(command, message, client_name):
    # Convert message to uppercase
    if command == "UPPER":
        return message.upper()
    
    # Convert message to lowercase
    elif command == "LOWER":
        return message.lower()
    
    # Reverse the message string
    elif command == "REVERSE":
        return message[::-1]
    
    # Count number of characters in message
    elif command == "COUNT":
        return str(len(message))
    
    # Count number of vowels in message
    elif command == "VOWELS":
        vowels = "aeiouAEIOU"
        return str(sum(1 for c in message if c in vowels))
    
    # Return current time
    elif command == "TIME":
        return datetime.now().strftime("%H:%M:%S")
    
    # Return current date
    elif command == "DATE":
        return datetime.now().strftime("%Y-%m-%d")
    
    # Handle unknown commands
    else:
        return f"ERROR: Unknown command from {client_name}."

def handle_client(conn, addr, client_name):
    # Print and log new connection
    print(f"{client_name} connected from {addr[0]}:{addr[1]}")
    log_to_file(f"{client_name} connected from {addr}")
    
    try:
        while True:
            # Receive data from client (max 1024 bytes)
            data = conn.recv(1024).decode().strip()
            
            # If no data, client disconnected
            if not data:
                break
            
            # If client sends QUIT, disconnect
            if data.upper() == "QUIT":
                print(f"{client_name} requested disconnect.")
                break
            
            # Validate message format (must contain ":")
            if ":" not in data:
                response = f"ERROR: Unknown command from {client_name}."
                conn.sendall(response.encode())
                continue
            
            # Split into command and message
            command, message = data.split(":", 1)
            command = command.strip().upper()  # Normalize command
            message = message.strip()  # Clean message remove spaces
            
            # Process command
            result = process_command(command, message, client_name)
            
        
            conn.sendall(result.encode())
            
            print(f"{client_name} sent: {command}: {message} → {result}")
            
            log_to_file(f"{client_name} sent: {command}: {message} -> {result}")
    
    except Exception as e:
      
        print(f"Error with {client_name}: {e}")
    
    finally:
       
        print(f"{client_name} disconnected.")
        log_to_file(f"{client_name} disconnected.")
        conn.close()

def start_server():
    global client_counter  # To modify global variable
    
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind server to IP and port
    server_socket.bind((HOST, PORT))
    
    # Start listening for incoming connections
    server_socket.listen()
    print(f"Server started on port {PORT}")
    
    while True:
        # Accept new client connection
        conn, addr = server_socket.accept()
        
        # Safely increment client counter
        with counter_lock:
            client_counter += 1
            client_name = f"Client{client_counter}"
        
        # Create new thread for each client
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, client_name)
        )
        
        # Start the thread
        thread.start()

# Entry point of the program
if __name__ == "__main__":
    start_server()