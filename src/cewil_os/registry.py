from dataclasses import dataclass

@dataclass(frozen=True)
class AgentDomain:
    id: str
    name: str
    description: str
    requires_professional_review: bool = True

AGENTS = (
    AgentDomain("practice-workflow", "Civil Engineering Practice Workflow", "Coordinates common civil-engineering practice workflows."),
    AgentDomain("construction-quality", "Construction Execution and Quality Control", "Supports execution records, inspections, and quality workflows."),
    AgentDomain("structural-design", "Structural Design (RC and Steel)", "Organises structural design inputs and review workflows."),
    AgentDomain("estimation-boq", "Building Estimation, BOQ, Rate Analysis", "Supports quantity take-off and estimation workflows."),
    AgentDomain("approvals-compliance", "Construction Approvals and Municipal Compliance", "Tracks approval requirements and compliance evidence."),
    AgentDomain("structural-audit", "Structural Auditing of Existing Buildings", "Organises existing-building inspection and audit evidence."),
    AgentDomain("concrete-guidance", "On-site Concrete Strength and Construction-Practice Guidance", "Organises concrete test data and construction-practice references."),
    AgentDomain("health-monitoring", "Structural Health Monitoring", "Tracks monitoring observations and trends."),
    AgentDomain("internship-mentoring", "Civil Engineering Student Internship Mentoring", "Supports structured student mentoring workflows."),
    AgentDomain("final-year-projects", "Final-Year Civil Engineering Project Assistance", "Supports academic project planning and documentation."),
)

BY_ID = {agent.id: agent for agent in AGENTS}
