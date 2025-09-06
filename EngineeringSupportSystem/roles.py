# roles.py
# Each action is (action_key, label). You can wire these to real handlers later.
ROLE_ACTIONS = {
    "admin": [
        ("view_all_tasks", "View All Tasks"),
        ("manage_users", "Manage Users"),
        ("approve_reject", "Approve / Reject Tasks"),
    ],
    "engineer": [
        ("view_my_tasks", "View My Tasks"),
        ("mark_complete", "Mark Selected Task Completed"),
    ],
    "supervisor": [
        ("view_progress", "View Engineers’ Progress"),
        ("approve_reject_completed", "Approve/Reject Completed"),
    ],
    "inspector": [
        ("safety_checklist", "Safety Inspection Checklist"),
        ("submit_inspection", "Submit Inspection Report"),
    ],
    "technician": [
        ("repair_requests", "View Repair Requests"),
        ("update_repair_status", "Update Repair Status"),
    ],
    "planner": [
        ("create_task", "Create Maintenance Task"),
        ("assign_task", "Assign Tasks to Engineers"),
    ],
    "qualitycontrol": [
        ("qc_checks", "Perform Quality Checks"),
        ("qc_approve", "Approve/Reject by QC"),
    ],
    "manager": [
        ("team_reports", "Team Performance Reports"),
        ("assign_roles", "Assign Roles to Staff"),
    ],
    "viewer": [
        ("view_tasks_reports", "View Tasks & Reports (Read-Only)"),
    ],
    # New 10 roles
    "scheduler": [
        ("maintenance_calendar", "Maintenance Calendar"),
        ("crew_rotation", "Crew Rotation Planning"),
    ],
    "safetyofficer": [
        ("safety_audit", "Run Safety Audit"),
        ("hazard_log", "Manage Hazard Log"),
    ],
    "logistics": [
        ("hangar_logistics", "Hangar Logistics"),
        ("shipping", "Parts Shipping"),
    ],
    "inventorymanager": [
        ("stock_levels", "Check Stock Levels"),
        ("reorder_parts", "Reorder Parts"),
    ],
    "documentation": [
        ("manuals", "Manage Manuals"),
        ("procedures", "Update Procedures"),
    ],
    "trainingcoordinator": [
        ("training_schedule", "Training Schedule"),
        ("cert_tracking", "Certification Tracking"),
    ],
    "flightops": [
        ("turnarounds", "Turnaround Coordination"),
        ("flight_schedule_sync", "Flight Schedule Sync"),
    ],
    "complianceofficer": [
        ("reg_checks", "Regulatory Checks"),
        ("audit_prep", "Audit Preparation"),
    ],
    "dataanalyst": [
        ("dashboards", "Analytics Dashboards"),
        ("export_reports", "Export KPI Reports"),
    ],
    "helpdesk": [
        ("ticket_queue", "Helpdesk Ticket Queue"),
        ("route_requests", "Route Requests"),
    ],
}

ROLE_PERMS = {
    # Core booleans used in UI
    # can_assign: show Assign button / action
    # can_mark_complete: allow marking completion
    # can_manage_users: show Manage Users
    # can_create_task: show Create Work Order
    "admin":             {"can_assign": True,  "can_mark_complete": True,  "can_manage_users": True,  "can_create_task": True},
    "manager":           {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": True},
    "planner":           {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": True},
    "engineer":          {"can_assign": False, "can_mark_complete": True,  "can_manage_users": False, "can_create_task": False},
    "technician":        {"can_assign": False, "can_mark_complete": True,  "can_manage_users": False, "can_create_task": False},
    "supervisor":        {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "qualitycontrol":    {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "inspector":         {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "viewer":            {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "scheduler":         {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "safetyofficer":     {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "logistics":         {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "inventorymanager":  {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "documentation":     {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "trainingcoordinator":{"can_assign": True, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "flightops":         {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "complianceofficer": {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "dataanalyst":       {"can_assign": False, "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
    "helpdesk":          {"can_assign": True,  "can_mark_complete": False, "can_manage_users": False, "can_create_task": False},
}
