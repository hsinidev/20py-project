import stem.process
from stem.util import term
import requests
import socks
import socket
import time
import threading

class TorManager:
    def __init__(self, socks_port=9050, control_port=9051):
        self.socks_port = socks_port
        self.control_port = control_port
        self.tor_process = None
        self.is_connected = False

    def start_tor(self, logger_callback=None):
        """Starts a local Tor process or connects to an existing one."""
        if logger_callback:
            logger_callback("[*] Initializing Tor Gateway...")
        
        try:
            # For this implementation, we assume Tor is either running or we simulate connection
            # In a real EXE distribution, we would bundle the tor binary
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", self.socks_port)
            socket.socket = socks.socksocket
            
            # Test connection
            response = requests.get("http://httpbin.org/ip", timeout=10)
            if logger_callback:
                logger_callback(f"[+] Tor Tunnel Active. IP: {response.json()['origin']}")
            self.is_connected = True
            return True
        except Exception as e:
            if logger_callback:
                logger_callback(f"[!] Tor Connection Failed: {str(e)}")
            self.is_connected = False
            return False

    def query_onion(self, url):
        """Wrapper for making safe requests to onion addresses."""
        try:
            session = requests.Session()
            session.proxies = {
                'http': f'socks5h://127.0.0.1:{self.socks_port}',
                'https': f'socks5h://127.0.0.1:{self.socks_port}'
            }
            return session.get(url, timeout=30).text
        except Exception as e:
            return f"Error: {str(e)}"

    def shutdown(self):
        if self.tor_process:
            self.tor_process.terminate()
        self.is_connected = False
