# Advanced SSH Agent Management

Your task is to write a simple program that interacts with a Unix Domain Socket using a custom protocol. The program should bind to a specified socket path, read incoming messages according to the protocol, process these messages, and respond appropriately.

**Inputs**

- **Socket Path**: The path to the Unix Domain Socket where the program will bind and listen for messages.
- **File Path**: The file to which content should be written or cleared based on the message type. This file path is provided as an argument when the program is launched.

**Protocol Specification**
Messages follow a custom protocol with the following structure:

- **First Byte**: Message Type
- **Bytes 2-4**: Reserved
- **Bytes 5-8**: Content-Length (4 bytes, big-endian)
- **Bytes 9+**: Content

Implement the following message types:

1. **0x1: Ok**

   - **Content Length:** Must be 0.
   - **Response:** If valid, no response is sent; if invalid, respond with an error.

2. **0x2: Write**

   - **Content:** The input should be appended to the provided file.
   - **Response:** Respond with Ok or Error based on the success or failure of the operation.

3. **0x3: Clear**

   - **Content Length:** Must be 0.
   - **Response:** The specified file is cleared. Respond with Ok or Error.

4. **0x4: Error**

   - **Content:** Indicates that something did not work as expected. The message is optional.

5. **0x5: Ping**
   - **Content Length:** Must be 0.
   - **Response:** If valid, respond with Ok; otherwise, respond with an error.

### How to run the program

**Open terminal 1**

```
python3 unix_socket_server.py /path/to/output/file.txt
```

**Open terminal 2**

1. Send an Ok Message (Type 0x1)

```
# Format: \x01 is the message type, reserved bytes \x00\x00\x00, content length \x00\x00\x00\x00
printf "\x01\x00\x00\x00\x00\x00\x00\x00" | socat - UNIX-CONNECT:/tmp/my_socket.sock
```

2. Send a Write Message (Type 0x2)

```
# Format: \x02 is message type, reserved bytes, content length (12 in this case, 0x0000000C in hex), and content "Hello, world"
printf "\x02\x00\x00\x00\x00\x00\x00\x0CHello, world" | socat - UNIX-CONNECT:/tmp/my_socket.sock
```

3. Send a Clear Message (Type 0x3)

```
# Format: \x03 for message type, reserved bytes, and content length of 0
printf "\x03\x00\x00\x00\x00\x00\x00\x00" | socat - UNIX-CONNECT:/tmp/my_socket.sock
```

4. Send a Ping Message (Type 0x5)

```
# Format: \x05 for message type, reserved bytes, and content length of 0
printf "\x05\x00\x00\x00\x00\x00\x00\x00" | socat - UNIX-CONNECT:/tmp/my_socket.sock
```

5. Send an Invalid Message Type

```
# Format: \xFF for unknown message type, reserved bytes, content length of 0
printf "\xFF\x00\x00\x00\x00\x00\x00\x00" | socat - UNIX-CONNECT:/tmp/my_socket.sock
```
