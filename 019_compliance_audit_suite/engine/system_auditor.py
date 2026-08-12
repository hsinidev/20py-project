import winreg
import psutil
import platform

class SystemAuditor:
    """
    Asynchronous scanner that verifies technical controls on the local system.
    """
    def __init__(self):
        self.os_type = platform.system()

    def run_check(self, check_config):
        """
        Executes a specific check based on config.
        """
        if "registry_key" in check_config:
            return self._check_registry(check_config)
        elif "service_status" in check_config:
            return self._check_service(check_config)
        return False, "Unknown check type"

    def _check_registry(self, config):
        try:
            path = config['registry_key']
            name = config['value_name']
            expected = config['expected']
            
            # Simple splitter for HKLM/HKCU
            root_str, sub_key = path.split('\\', 1)
            root = winreg.HKEY_LOCAL_MACHINE if root_str == "HKLM" else winreg.HKEY_CURRENT_USER
            
            with winreg.OpenKey(root, sub_key) as key:
                value, _ = winreg.QueryValueEx(key, name)
                if value == expected:
                    return True, f"Value matches expected: {value}"
                else:
                    return False, f"Mismatch. Expected {expected}, got {value}"
        except Exception as e:
            return False, f"Registry error: {str(e)}"

    def _check_service(self, config):
        try:
            service_name = config['service_status']
            expected = config['expected']
            
            for service in psutil.win_service_iter():
                if service.name() == service_name:
                    status = service.status()
                    if status.lower() == expected.lower():
                        return True, f"Service '{service_name}' is {status}"
                    else:
                        return False, f"Service '{service_name}' is {status}, expected {expected}"
            return False, f"Service '{service_name}' not found"
        except Exception as e:
            return False, f"Service check error: {str(e)}"
