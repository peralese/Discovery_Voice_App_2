# context_manager.py
# Manages discovery schema state during the dynamic interview

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

def init_context():
    # Returns a fresh copy of the discovery schema
    return discovery_schema.copy()

def is_complete(context):
    # Returns True if all values are filled
    return all(value is not None and value.strip() != "" for value in context.values())

def get_missing_fields(context):
    return [field for field, value in context.items() if value is None or value.strip() == ""]

def update_context(context, field, value):
    if field in context:
        context[field] = value.strip()
