from typing import TypedDict, Literal, Optional

Role = Literal[
    "admin","engineer","supervisor","inspector","technician","planner",
    "qualitycontrol","manager","viewer",
    "scheduler","safetyofficer","logistics","inventorymanager","documentation",
    "trainingcoordinator","flightops","complianceofficer","dataanalyst","helpdesk"
]

class User(TypedDict):
    username: str
    password: str
    role: Role

class Task(TypedDict, total=False):
    id: int
    title: str
    details: str
    assigned_to: Optional[str]
    status: str  # pending|in_progress|completed|approved|rejected|in_review
    base_id: str             # e.g., "OOMS"
    aircraft_tail: str       # e.g., "A6-ABC"