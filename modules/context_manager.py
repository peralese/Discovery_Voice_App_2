# context_manager.py
# Manages discovery schema state during the dynamic interview

# modules/context_manager.py

discovery_schema = {
    "interviewee_name": None,
    "application_name": None,
    "architecture_overview": None,
    "business_processes": None,
    "user_concurrency": None,
    "databases": None,
    "technology_stack": None,
    "current_hosting": None,
    "security_compliance": None,
    "deployment_process": None,
    "sla_metrics": None,
    "backup_strategy": None,
    "known_issues": None
}

import json

class DiscoveryContext:
    def __init__(self):
        self.context = discovery_schema.copy()

    def get_context(self):
        return self.context

    def is_complete(self):
        return all(value is not None and value.strip() != "" for value in self.context.values())

    def get_missing_fields(self):
        return [field for field, value in self.context.items() if value is None or value.strip() == ""]

    def update_context(self, user_response):
        # Naive mapping: fills the next unanswered field with the response
        for field in self.context:
            if self.context[field] is None:
                self.context[field] = user_response.strip()
                break

    def to_json(self):
        return json.dumps(self.context, indent=2)

    def save_to_file(self, filename):
        with open(filename, "w") as f:
            json.dump(self.context, f, indent=2)
