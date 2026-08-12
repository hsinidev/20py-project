import winreg
import psutil
import socket
import logging

class WindowsAdapter:
    """
    Native OS Interaction Layer for Registry, Services, and Port checks.
    """
    @staticmethod
    def check_registry(path, value_name, expected):
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            with winreg.OpenKey(reg, path) as key:
                value, _ = winreg.QueryValueEx(key, value_name)
                return value == expected
        except FileNotFoundError:
            # Key or Value does not exist, which means it doesn't match expected
            return False
        except Exception as e:
            logging.error(f"Registry check error on {path}: {e}")
            return False

    @staticmethod
    def check_service(service_name, expected_status):
        try:
            service = psutil.win_service_get(service_name)
            status = service.status()
            return status == expected_status
        except Exception:
            return False

    @staticmethod
    def check_port(port):
        """Checks if a local port is open."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex(('127.0.0.1', port))
            # result 0 means port is open
            return result != 0 # We expect it to be closed
