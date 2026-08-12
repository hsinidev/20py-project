class PolicyBenchmark:
    """
    Policy Definitions based on CIS (Center for Internet Security) Benchmarks.
    """
    POLICIES = {
        "workstation": [
            {
                "id": "POL-001",
                "name": "AutoRun Disabled",
                "check_type": "registry",
                "key": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer",
                "value": "NoDriveTypeAutoRun",
                "expected": 255,
                "description": "Ensure AutoRun is disabled for all drives to prevent malware propagation.",
                "remediation": "Set HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer -Name NoDriveTypeAutoRun -Value 255"
            },
            {
                "id": "POL-002",
                "name": "Firewall Enabled",
                "check_type": "service",
                "service_name": "mpssvc",
                "expected": "running",
                "description": "Windows Defender Firewall must be running.",
                "remediation": "Start-Service mpssvc; Set-Service mpssvc -StartupType Automatic"
            },
            {
                "id": "POL-003",
                "name": "Remote Desktop Disabled",
                "check_type": "registry",
                "key": r"SYSTEM\CurrentControlSet\Control\Terminal Server",
                "value": "fDenyTSConnections",
                "expected": 1,
                "description": "Remote Desktop should be disabled unless strictly necessary.",
                "remediation": "Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 1"
            },
            {
                "id": "POL-004",
                "name": "Unnecessary Port Check (Port 21)",
                "check_type": "port",
                "port": 21,
                "expected": "closed",
                "description": "FTP Port 21 should be closed to prevent insecure file transfers.",
                "remediation": "Disable-NetFirewallRule -Name 'FTP-In-TCP'"
            }
        ],
        "server": [
            # More aggressive policies for servers
        ]
    }

    @staticmethod
    def get_policies(profile="workstation"):
        return PolicyBenchmark.POLICIES.get(profile, PolicyBenchmark.POLICIES["workstation"])
