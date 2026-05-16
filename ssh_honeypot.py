import logging
from logging.handlers import RotatingFileHandler
import socket
import paramiko
import threading
import os

logging_format = logging.Formatter('%(message)s')

SSH_BANNER = "SSH-2.0-MySSHServer_1.0"

if not os.path.exists('server.key'):
    new_key = paramiko.RSAKey.generate(2048)
    new_key.write_private_key_file('server.key')
    print("Generated new server.key")

host_key = paramiko.RSAKey(filename='server.key')

funnel_logger = logging.getLogger('FunnelLogger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)


def emulated_shell(channel, client_ip):
    channel.send(b'bruhwhatisthis$ ')
    command = b""
    while True:
        char = channel.recv(1)
        if not char:
            channel.close()
            break

        channel.send(char)
        command += char

        if char == b'\r':
            if command.strip() == b'exit':
                channel.send(b'\nGoodbye!\n')
                channel.close()
                break

            elif command.strip() == b'pwd':
                response = b'\n\\usr\\local\\' + b'\r\n'
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b'whoami':
                response = b"\n" + b"bruh" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b'ls':
                response = b"\n" + b"whatisthis.conf" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            elif command.strip() == b"cat whatisthis.conf":
                response = b"\n" + b"Go to whatisthis.com" + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            else:
                response = b"\n" + bytes(command.strip()) + b"\r\n"
                creds_logger.info(f'Command {command.strip()}' + 'executed by ' + f'{client_ip}')
            channel.send(response)
            channel.send(b'bruhwhatisthis$ ')
            command = b""


class Server(paramiko.ServerInterface):
    def __init__(self, client_ip, input_username=None, input_password=None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return "password"

    def check_auth_password(self, username, password):
        funnel_logger.info(f'Client {self.client_ip} attempted login with username: {username}, password: {password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_exec_request(self, channel, command):
        command = str(command)
        creds_logger.info(f'Exec command attempted: {command} from {self.client_ip}')
        return True


def client_handle(client, addr, username, password):
    client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")
    transport = None
    try:
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER

        server = Server(client_ip=client_ip, input_username=username, input_password=password)
        transport.add_server_key(host_key)

        try:
            transport.start_server(server=server)
        except paramiko.SSHException as e:
            print(f"[{client_ip}] SSH negotiation failed: {e}")
            return

        channel = transport.accept(100)
        if channel is None:
            print(f"[{client_ip}] No channel was opened.")
            return

        server.event.wait(10)
        if not server.event.is_set():
            print(f"[{client_ip}] Client never requested a shell.")
            channel.close()
            return

        standard_banner = b"Welcome to my humble abode.\r\n"
        channel.send(standard_banner)
        emulated_shell(channel, client_ip=client_ip)

    except Exception as error:
        print(f"[{client_ip}] Error: {error}")
    finally:
        if transport:
            try:
                transport.close()
            except Exception as error:
                print(f"[{client_ip}] Cleanup error: {error}")
        client.close()


def honeypot(address, port, username, password):
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))
    socks.listen(100)
    print(f"SSH server is listening on port {port}.")

    while True:
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))
            ssh_honeypot_thread.daemon = True
            ssh_honeypot_thread.start()
        except Exception as error:
            print(f"Honeypot error: {error}")


#honeypot('0.0.0.0', 2223, username = None, password = None)