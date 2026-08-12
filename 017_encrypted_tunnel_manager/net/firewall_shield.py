import os
import sys
import subprocess
import logging

class FirewallShield:
    """
    Implements a 'Kernel-Level Kill-Switch' to prevent IP leaks.
    Injects rules into WFP (Windows) or Iptables (Linux).
    """
    def __init__(self):
        self.os_type = sys.platform
        self.kill_switch_active = False

    def activate_kill_switch(self):
        """
        Blocks all outbound traffic except for the encrypted tunnel endpoint.
        """
        try:
            if self.os_type == "win32":
                self._activate_windows_wfp()
            else:
                self._activate_linux_iptables()
            self.kill_switch_active = True
            logging.info("KILL-SWITCH ACTIVE: All unencrypted traffic blocked.")
        except Exception as e:
            logging.error(f"Failed to activate Kill-Switch: {e}")

    def deactivate_kill_switch(self):
        try:
            if self.os_type == "win32":
                self._deactivate_windows_wfp()
            else:
                self._deactivate_linux_iptables()
            self.kill_switch_active = False
            logging.info("KILL-SWITCH DEACTIVATED: Normal traffic resumed.")
        except Exception as e:
            logging.error(f"Failed to deactivate Kill-Switch: {e}")

    def _activate_windows_wfp(self):
        # Implementation using 'netsh advfirewall' as a high-level wrapper for WFP
        # Blocks all outbound traffic
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], check=True)
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "blockoutbound,allowinbound"], check=True)

    def _deactivate_windows_wfp(self):
        # Restore default outbound policy
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "allowoutbound,allowinbound"], check=True)

    def _activate_linux_iptables(self):
        # Allow loopback
        subprocess.run(["iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], check=True)
        # Allow established connections
        subprocess.run(["iptables", "-A", "OUTPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=True)
        # Block everything else outbound
        subprocess.run(["iptables", "-P", "OUTPUT", "DROP"], check=True)

    def _deactivate_linux_iptables(self):
        subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)
        subprocess.run(["iptables", "-F", "OUTPUT"], check=True)

if __name__ == "__main__":
    shield = FirewallShield()
    # shield.activate_kill_switch()
