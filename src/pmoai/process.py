from enum import Enum


class Process(str, Enum):
    """Enum for different process flows in PMOAI.

    Attributes:
        sequential: Tasks are executed in sequence, with each task's output available to subsequent tasks.
        hierarchical: A manager agent delegates tasks to other agents and synthesizes their outputs.
        agile: Tasks are executed in sprints with regular review and adaptation.
        waterfall: Tasks are executed in distinct phases with formal approvals between phases.
        kanban: Tasks are pulled through workflow stages based on capacity.
        hybrid: A combination of agile and waterfall approaches.
    """

    sequential = "sequential"
    hierarchical = "hierarchical"
    agile = "agile"
    waterfall = "waterfall"
    kanban = "kanban"
    hybrid = "hybrid"
