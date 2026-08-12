import yaml
import os

class FrameworkManager:
    """
    Loads and manages compliance frameworks (ISO 27001, SOC2).
    """
    def __init__(self, framework_path):
        self.framework_path = framework_path
        self.data = self._load_framework()
        self.controls = self.data.get('controls', [])

    def _load_framework(self):
        if not os.path.exists(self.framework_path):
            return {"framework": "Unknown", "controls": []}
        
        with open(self.framework_path, 'r') as f:
            return yaml.safe_load(f)

    def get_control_by_id(self, control_id):
        for control in self.controls:
            if control['id'] == control_id:
                return control
        return None

    def get_categories(self):
        return list(set(c['category'] for c in self.controls))
