import sys
import logging
from core.ssh_manager import SSHManager
from net.firewall_shield import FirewallShield
from net.traffic_analyzer import TrafficAnalyzer
from ui.dashboard import TunnelDashboard

def main():
    # Setup Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Initialize Core Engines
    analyzer = TrafficAnalyzer()
    analyzer.start_monitoring()
    
    shield = FirewallShield()
    
    # Initialize UI
    dashboard = TunnelDashboard(analyzer)
    
    try:
        dashboard.run()
    except KeyboardInterrupt:
        pass
    finally:
        analyzer.stop_monitoring()
        if shield.kill_switch_active:
            shield.deactivate_kill_switch()
        logging.info("System Shutdown.")

if __name__ == "__main__":
    main()
