# Multi-clients-processing-server-for-networks-
Multi clients processing server  python for computer networks 
# Multi-Client TCP Command Server

A simple multi-threaded TCP server and client built with Python sockets. The server accepts multiple simultaneous client connections, processes text commands (case conversion, reversal, counting, vowel counting, time/date lookup), and logs all activity to a file.

## Features

- **Multi-client support** — each client connection is handled in its own thread, so multiple users can connect and chat with the server at the same time.
- **Thread-safe client naming** — clients are automatically assigned sequential names (`Client1`, `Client2`, ...) using a lock to avoid naming collisions.
- **Thread-safe logging** — all activity is timestamped and written to `server_log.txt` using a lock to prevent file corruption when multiple threads write at once.
- **Simple command protocol** — clients send commands in the format `COMMAND:MESSAGE` and receive a processed response.
- **Graceful disconnects** — clients can quit at any time with `QUIT`, and the server cleans up connections safely.

## Supported Commands

| Command   | Description                          | Example Input     | Example Output |
|-----------|---------------------------------------|--------------------|-----------------|
| `UPPER`   | Converts text to uppercase            | `UPPER:hello`      | `HELLO`         |
| `LOWER`   | Converts text to lowercase            | `LOWER:HELLO`      | `hello`         |
| `REVERSE` | Reverses the message                  | `REVERSE:hello`    | `olleh`         |
| `COUNT`   | Counts characters in the message      | `COUNT:hello`      | `5`             |
| `VOWELS`  | Counts vowels (a, e, i, o, u)         | `VOWELS:hello`     | `2`             |
| `TIME`    | Returns the server's current time     | `TIME:`             | `14:32:10`      |
| `DATE`    | Returns the server's current date     | `DATE:`             | `2026-07-21`    |
| `QUIT`    | Disconnects the client                | `QUIT`             | —               |

Any unrecognized command returns an error message:
`ERROR: Unknown command from <client_name>.`

## How It Works

### Server (`server.py`)

1. Creates a TCP socket, binds it to `127.0.0.1:4949`, and listens for incoming connections.
2. On each new connection, assigns the client a unique name (`Client1`, `Client2`, ...) using a thread lock to prevent duplicate names.
3. Spawns a new thread per client via `handle_client()`, allowing multiple clients to be served concurrently.
4. Inside each client thread:
   - Waits for incoming data (`COMMAND:MESSAGE` format).
   - Validates the format and splits it into `command` and `message`.
   - Passes it to `process_command()` to get the result.
   - Sends the result back to the client.
   - Logs the interaction (console + `server_log.txt`) with a timestamp.
   - Exits the loop and closes the connection on `QUIT` or empty data (client disconnect).
5. Handles exceptions gracefully and always closes the connection in a cleanup step.

### Client (`client.py`)

1. Creates a TCP socket and connects to the server at `127.0.0.1:4949`.
2. Displays available commands and prompts the user for input.
3. Sends the raw command string to the server (encoded to bytes).
4. Waits for and prints the server's response (decoded from bytes).
5. Repeats until the user enters `QUIT`, which sends the quit signal to the server before exiting.
6. Handles `ConnectionRefusedError` if the server isn't running, and always closes the socket in a `finally` block.

## Getting Started

### Requirements

- Python 3.x (no external dependencies — uses only the standard library: `socket`, `threading`, `datetime`)

### Running the Server

```bash
python server.py
```

The server will start listening on `127.0.0.1:4949` and print connection/activity logs to the console. All activity is also saved to `server_log.txt`.

### Running the Client

In a separate terminal:

```bash
python client.py
```

Once connected, enter commands in the format:

```
COMMAND:MESSAGE
```

For example:

```
> UPPER:hello world
Response from server: HELLO WORLD
```

To disconnect, type:

```
> QUIT
```

You can run multiple client instances simultaneously to test the server's multi-threading support — each will be assigned its own client name and handled independently.

- `HOST` and `PORT` must match exactly between `server.py` and `client.py` (`127.0.0.1:4949` by default).
- Locks (`counter_lock`, `log_lock`) are used to keep client numbering and log writes safe under concurrent access from multiple threads.
- This project is intended as a learning example for TCP sockets, multi-threading, and basic client-server protocols in Python.
