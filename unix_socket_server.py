import socket
import struct
import os
import sys

# Define message types as constants
MSG_OK = 0x1
MSG_WRITE = 0x2
MSG_CLEAR = 0x3
MSG_ERROR = 0x4
MSG_PING = 0x5

# Define socket path
SOCKET_PATH = '/tmp/my_socket.sock'

def create_server_socket(socket_path):
    """Create and return a server Unix Domain Socket bound to the specified path."""
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.unlink(socket_path)  # Remove any existing socket
    except FileNotFoundError:
        pass
    server_socket.bind(socket_path)
    server_socket.listen(1)
    print(f"Server listening on {socket_path}")
    return server_socket

def handle_client_connection(client_socket, file_path):
    """Process incoming messages from the client according to the protocol."""
    while True:
        try:
            # Read the first 8 bytes (header)
            header = client_socket.recv(8)
            if len(header) < 8:
                break  # Connection closed or incomplete message
            
            # Parse the header
            message_type = header[0]
            reserved = header[1:4]
            content_length = struct.unpack('>I', header[4:8])[0]
            
            # Read the content based on content length
            content = client_socket.recv(content_length) if content_length > 0 else b''
            
            # Process message based on type
            if message_type == MSG_OK:
                if content_length != 0:
                    send_error(client_socket, "Invalid content length for Ok.")
            elif message_type == MSG_WRITE:
                append_to_file(file_path, content)
                send_ok(client_socket)
            elif message_type == MSG_CLEAR:
                clear_file(file_path)
                send_ok(client_socket)
            elif message_type == MSG_PING:
                if content_length != 0:
                    send_error(client_socket, "Invalid content length for Ping.")
                else:
                    send_ok(client_socket)
            else:
                send_error(client_socket, "Unknown message type.")
        
        except Exception as e:
            send_error(client_socket, f"Server error: {str(e)}")
            break

def append_to_file(file_path, content):
    """Append the content to the specified file."""
    try:
        with open(file_path, 'ab') as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Failed to write to file: {str(e)}")

def clear_file(file_path):
    """Clear the specified file."""
    try:
        open(file_path, 'w').close()
    except Exception as e:
        raise IOError(f"Failed to clear file: {str(e)}")

def send_ok(client_socket):
    """Send an Ok message with no content."""
    client_socket.sendall(struct.pack('>B3xI', MSG_OK, 0))

def send_error(client_socket, error_message):
    """Send an Error message with the provided error content."""
    content = error_message.encode('utf-8')
    client_socket.sendall(struct.pack('>B3xI', MSG_ERROR, len(content)) + content)

def main(file_path):
    """Main function to run the Unix Domain Socket server."""
    # Create and bind the server socket
    server_socket = create_server_socket(SOCKET_PATH)
    
    try:
        while True:
            # Accept and handle client connections
            client_socket, _ = server_socket.accept()
            with client_socket:
                handle_client_connection(client_socket, file_path)
    finally:
        # Clean up socket
        server_socket.close()
        os.unlink(SOCKET_PATH)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unix_socket_server.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    main(file_path)
