from config import SSH_HOST, SSH_PORT, ALLOWED_USERNAME, SSH_KEY
from logger import log_connection, log_login
from detector import detect_bruteforce
import socket
import paramiko
import threading
from geoip import get_location

key_file = SSH_KEY
try:
    HOST_KEY = paramiko.RSAKey(filename=key_file)
except FileNotFoundError:
    HOST_KEY = paramiko.RSAKey.generate(2048)
    HOST_KEY.write_private_key_file(key_file)

class SSHServer(paramiko.ServerInterface):
    def check_auth_password(self, username, password) -> int:
        if username not in ALLOWED_USERNAME:
            print(f"[!] Failed login attempt: {username}:{password}")
            log_login(username, password, 0)
            return paramiko.AUTH_FAILED
        else:
            print(f"[+] Success login attempt: {username}:{password}")
            log_login(username, password, 1)
            global usr
            usr = username
            return paramiko.AUTH_SUCCESSFUL
        
    def get_allowed_auths(self, username) -> str:
        return super().get_allowed_auths(username)
    
    def check_channel_request(self, kind, chanid) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        else:
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_pty_request(self, channel: paramiko.Channel, term: bytes, width, height, pixelwidth, pixelheight, modes: bytes) -> bool:
        return True
    
    def check_channel_shell_request(self, channel: paramiko.Channel) -> bool:
        return True
    
    def check_channel_exec_request(self, channel: paramiko.Channel, command: bytes) -> bool:
        return True
    
    def check_channel_subsystem_request(self, channel: paramiko.Channel, name) -> bool:
        return False


def handle_client(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    sshserver = SSHServer()
    input_buffer = ""
    try:
        transport.start_server(server=sshserver)
        channel = transport.accept(20)

        if channel == None:
            raise Exception("No channel")
            
        print("[+] Client connected")
        channel.send("Welcome to Ubuntu 15.04 (GNU/Linux 3.19.0-15-generic x86_64)\n\r")
        channel.send(f"{usr}@{SSH_HOST}:~$ ")

        while True:
            try:
                data = channel.recv(1024).decode(errors="ignore").strip()
                if not data:
                    continue

                if data == "\x7f" and len(input_buffer) > 0:
                    input_buffer = input_buffer[:-1]
                    channel.send("\b \b")
                elif data == "\x7f" and len(input_buffer) < 1:
                    continue
                else:
                    input_buffer += data
                    channel.send(data)
            except Exception as i:
                print(f"[!] Error on fetching client prompt: {i}")
                break
    except Exception as i:
        print(f"[!] Exception on Transport: {i}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SSH_HOST, SSH_PORT))
    server.listen(20)
    print(f"Server listening on {SSH_HOST}:{SSH_PORT}")

    while True:
        client, addr = server.accept()

        try:
            city, country = get_location(addr[0])
        except:
            city, country = ("Not found", "Not found")
            print(f"[!] Failed to fetch geolocation ({addr[0]})")
            pass

        print(f"[+] Connection from {addr[0]} ({city}, {country})")
        log_connection(addr[0], city, country)
        detect_bruteforce(addr[0])
        t = threading.Thread(target=handle_client, args=(client,))
        t.start()
        

if __name__ == "__main__":
    main()