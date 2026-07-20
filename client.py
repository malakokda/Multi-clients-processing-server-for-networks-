import socket 

def start_client():
    # Server IP (localhost means same computer)
    HOST = '127.0.0.1'
    
    # Port must match server port
    PORT = 4949

    # Create a TCP socket (SOCK_STREAM = TCP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server using IP and port
        client_socket.connect((HOST, PORT))
        print("Connected to server.")

        # Continuous loop to send multiple commands
        while True:
            # Show available commands to the user
            print("\nEnter command (UPPER/LOWER/REVERSE/COUNT/VOWELS/TIME/DATE/QUIT):")
            
            # Get user input and remove extra spaces
            user_input = input("> ").strip()

            # Validate empty input
            if not user_input:
                print("Invalid input. Try again.")
                continue

            # Send user input to server (encoded to bytes)
            client_socket.sendall(user_input.encode())

            # If user wants to quit, stop loop after sending
            if user_input.upper() == "QUIT":
                break

            # Receive response from server (max 1024 bytes)
            response = client_socket.recv(1024).decode()

            # Print server response
            print(f"Response from server: {response}")

    except ConnectionRefusedError:
        # Happens when server is not running or wrong port
        print("Server is not running.")

    finally:
        # Always close socket connection safely
        print("Connection closed.")
        client_socket.close()

# Entry point of the program
if __name__ == "__main__":
    start_client()