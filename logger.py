import logging
from config import SSH_LOG, BRUTEFORCE_LIST

paramiko_logger = logging.getLogger("paramiko")
paramiko_logger.setLevel(logging.WARNING)

class IgnoreSocketException(logging.Filter):
    def filter(self, record):
        return "Socket exception" not in record.getMessage()

paramiko_logger.addFilter(IgnoreSocketException())

my_logger = logging.getLogger("ssh_honeypot")
my_logger.setLevel(logging.INFO)
handler = logging.FileHandler(SSH_LOG)
handler.setFormatter(logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s"))
my_logger.addHandler(handler)

b_logger = logging.getLogger("bruteforce_logger")
b_logger.setLevel(logging.INFO)
handler1 = logging.FileHandler(BRUTEFORCE_LIST)
handler1.setFormatter(logging.Formatter("%(message)s"))
b_logger.addHandler(handler1)

def log_connection(ip, city, country):
    my_logger.info(f"[+] Connection from {ip} ({city}, {country})")

def log_login(username, password, status):
    if status == 1:
        my_logger.info(f"[+] Success login {username}:{password}")
    elif status == 0:
        my_logger.info(f"[!] Failed login {username}:{password}")

def log_bruteforce(ip):
    my_logger.info(f"[!] Possible bruteforce attack from {ip}")
    b_logger.info(ip)