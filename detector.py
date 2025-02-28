import time
from collections import defaultdict
from config import BRUTEFORCE_THRESHOLD
from logger import log_bruteforce

failed_attempts = defaultdict(list)

def detect_bruteforce(ip):
    now = time.time()
    failed_attempts[ip].append(now)
    if len(failed_attempts[ip]) > BRUTEFORCE_THRESHOLD:
        print(f"[!] Possible bruteforce attack from {ip}")
        log_bruteforce(ip)