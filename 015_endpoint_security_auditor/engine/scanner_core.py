import asyncio
from engine.adapters.windows_wmi import WindowsAdapter
from engine.cis_benchmarks import PolicyBenchmark
import logging

class AuditScanner:
    """
    Asynchronous Audit Controller for parallel scanning of security policies.
    """
    def __init__(self, profile="workstation"):
        self.policies = PolicyBenchmark.get_policies(profile)
        self.results = []

    async def run_check(self, policy):
        """Executes a single policy check asynchronously."""
        # Simulate slight delay for UI pulse effect
        await asyncio.sleep(0.5)
        
        status = False
        if policy["check_type"] == "registry":
            status = WindowsAdapter.check_registry(policy["key"], policy["value"], policy["expected"])
        elif policy["check_type"] == "service":
            status = WindowsAdapter.check_service(policy["service_name"], policy["expected"])
        elif policy["check_type"] == "port":
            status = WindowsAdapter.check_port(policy["port"])
            
        result = {
            "id": policy["id"],
            "name": policy["name"],
            "status": "PASS" if status else "FAIL",
            "description": policy["description"],
            "remediation": policy["remediation"] if not status else None
        }
        return result

    async def scan_all(self, progress_callback=None):
        """Scans all policies in parallel or sequence based on priority."""
        self.results = []
        total = len(self.policies)
        
        for i, policy in enumerate(self.policies):
            res = await self.run_check(policy)
            self.results.append(res)
            if progress_callback:
                progress_callback(res, (i + 1) / total)
                
        return self.results
