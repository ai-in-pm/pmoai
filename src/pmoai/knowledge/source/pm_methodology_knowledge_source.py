from typing import Any, Dict, List, Optional

from pydantic import Field

from pmoai.knowledge.source.base_knowledge_source import BaseKnowledgeSource


class PMMethodologyKnowledgeSource(BaseKnowledgeSource):
    """Knowledge source for project management methodologies.

    This class provides knowledge about different project management methodologies,
    including Agile, Waterfall, Kanban, and others.
    """

    methodology: str = Field(
        description="The project management methodology to provide knowledge about."
    )

    def __init__(self, methodology: str, **kwargs: Any):
        """Initialize the PM methodology knowledge source.

        Args:
            methodology: The project management methodology to provide knowledge about.
            **kwargs: Additional arguments to pass to the parent constructor.
        """
        super().__init__(**kwargs)
        self.methodology = methodology.lower()

    def add(self) -> None:
        """
        Add this knowledge source to the knowledge base.
        """
        if self.storage is None:
            raise ValueError("Storage is not initialized.")

        chunks = self.get_chunks()
        self.storage.add_texts(chunks, self.metadata)

    def get_content(self) -> str:
        """
        Get the content of this knowledge source.

        Returns:
            The content of this knowledge source.
        """
        return self.get_knowledge()

    def get_knowledge(self) -> str:
        """Get knowledge about the specified project management methodology.

        Returns:
            Knowledge about the project management methodology.
        """
        if self.methodology == "agile":
            return self._get_agile_knowledge()
        elif self.methodology == "waterfall":
            return self._get_waterfall_knowledge()
        elif self.methodology == "kanban":
            return self._get_kanban_knowledge()
        elif self.methodology == "scrum":
            return self._get_scrum_knowledge()
        elif self.methodology == "lean":
            return self._get_lean_knowledge()
        elif self.methodology == "prince2":
            return self._get_prince2_knowledge()
        elif self.methodology == "pmi":
            return self._get_pmi_knowledge()
        elif self.methodology == "hybrid":
            return self._get_hybrid_knowledge()
        else:
            return f"No knowledge available for methodology: {self.methodology}"

    def _get_agile_knowledge(self) -> str:
        """Get knowledge about Agile methodology.

        Returns:
            Knowledge about Agile methodology.
        """
        return """
# Agile Project Management Methodology

## Core Principles
- Individuals and interactions over processes and tools
- Working software over comprehensive documentation
- Customer collaboration over contract negotiation
- Responding to change over following a plan

## Key Practices
- Iterative development in short sprints (typically 2-4 weeks)
- Daily stand-up meetings
- Sprint planning and retrospectives
- Continuous integration and delivery
- User stories and acceptance criteria
- Backlog grooming and prioritization

## Frameworks
- Scrum
- Kanban
- Extreme Programming (XP)
- Crystal
- Feature-Driven Development (FDD)

## Roles
- Product Owner
- Scrum Master
- Development Team

## Artifacts
- Product Backlog
- Sprint Backlog
- Burndown Charts
- User Stories
- Definition of Done

## Benefits
- Flexibility and adaptability to change
- Regular delivery of working software
- Continuous feedback and improvement
- Enhanced collaboration and communication
- Higher customer satisfaction
- Early identification of issues and risks

## Challenges
- Requires active customer involvement
- May be difficult to scale for large projects
- Documentation may be less comprehensive
- Requires experienced team members
- May be challenging for fixed-price contracts
"""

    def _get_waterfall_knowledge(self) -> str:
        """Get knowledge about Waterfall methodology.

        Returns:
            Knowledge about Waterfall methodology.
        """
        return """
# Waterfall Project Management Methodology

## Core Principles
- Sequential, linear approach to project management
- Each phase must be completed before the next begins
- Comprehensive documentation at each phase
- Formal approval processes between phases

## Key Phases
1. Requirements
2. Design
3. Implementation
4. Verification
5. Maintenance

## Key Practices
- Detailed upfront planning
- Comprehensive documentation
- Formal change control processes
- Structured testing and validation
- Formal sign-offs between phases

## Roles
- Project Manager
- Business Analyst
- System Architect
- Developers
- Quality Assurance
- Stakeholders

## Artifacts
- Project Charter
- Requirements Document
- Design Specifications
- Test Plans
- Implementation Plan
- Maintenance Plan

## Benefits
- Clear structure and milestones
- Well-defined deliverables
- Comprehensive documentation
- Predictable timeline and budget
- Less customer involvement required during development
- Well-suited for projects with fixed requirements

## Challenges
- Limited flexibility for changes
- Late detection of issues
- Customer doesn't see working product until late in the process
- Risk of project failure if requirements are misunderstood
- May lead to longer project timelines
"""

    def _get_kanban_knowledge(self) -> str:
        """Get knowledge about Kanban methodology.

        Returns:
            Knowledge about Kanban methodology.
        """
        return """
# Kanban Project Management Methodology

## Core Principles
- Visualize workflow
- Limit work in progress (WIP)
- Manage flow
- Make process policies explicit
- Implement feedback loops
- Improve collaboratively, evolve experimentally

## Key Practices
- Kanban board to visualize work
- WIP limits for each workflow stage
- Pull system for work items
- Continuous flow of work
- Metrics and analytics for process improvement
- Regular cadence of delivery

## Components
- Kanban Board
- Cards/Tickets
- Columns/Lanes
- WIP Limits
- Swimlanes
- Classes of Service

## Metrics
- Lead Time
- Cycle Time
- Throughput
- Cumulative Flow Diagram
- Flow Efficiency
- Blocked Time

## Benefits
- Flexibility and adaptability
- Reduced waste and overhead
- Improved predictability
- Better visibility of work
- Continuous delivery
- Evolutionary change with minimal resistance
- Focus on flow and quality

## Challenges
- May lack timeboxing and regular cadence
- Requires discipline to maintain WIP limits
- May be difficult to plan long-term
- Less structured than other methodologies
- May not provide clear roles and responsibilities
"""

    def _get_scrum_knowledge(self) -> str:
        """Get knowledge about Scrum methodology.

        Returns:
            Knowledge about Scrum methodology.
        """
        return """
# Scrum Project Management Methodology

## Core Principles
- Empirical process control (transparency, inspection, adaptation)
- Self-organization
- Collaboration
- Time-boxing
- Iterative development
- Incremental delivery

## Key Events
- Sprint (1-4 weeks)
- Sprint Planning
- Daily Scrum (Daily Stand-up)
- Sprint Review
- Sprint Retrospective
- Backlog Refinement

## Roles
- Product Owner
- Scrum Master
- Development Team

## Artifacts
- Product Backlog
- Sprint Backlog
- Increment
- Burndown/Burnup Charts
- Definition of Done

## Benefits
- Regular delivery of working software
- Adaptability to changing requirements
- Enhanced team collaboration
- Continuous improvement
- Early identification of issues and risks
- Clear roles and responsibilities
- Predictable delivery cadence

## Challenges
- Requires experienced Scrum Master and Product Owner
- May be difficult to scale for large projects
- Requires full team commitment
- May be challenging for distributed teams
- Requires cultural shift for traditional organizations
"""

    def _get_lean_knowledge(self) -> str:
        """Get knowledge about Lean methodology.

        Returns:
            Knowledge about Lean methodology.
        """
        return """
# Lean Project Management Methodology

## Core Principles
- Eliminate waste
- Build quality in
- Create knowledge
- Defer commitment
- Deliver fast
- Respect people
- Optimize the whole

## Key Practices
- Value stream mapping
- Just-in-time delivery
- Pull systems
- Continuous improvement (Kaizen)
- Root cause analysis
- Visual management
- Small batch sizes

## Types of Waste (DOWNTIME)
- Defects
- Overproduction
- Waiting
- Non-utilized talent
- Transportation
- Inventory
- Motion
- Extra processing

## Tools and Techniques
- 5S (Sort, Set in order, Shine, Standardize, Sustain)
- Kanban boards
- A3 problem solving
- Gemba walks
- Poka-yoke (error-proofing)
- PDCA (Plan-Do-Check-Act) cycles
- Heijunka (production leveling)

## Benefits
- Reduced waste and costs
- Improved quality
- Faster delivery
- Enhanced customer satisfaction
- Continuous improvement culture
- Empowered teams
- Sustainable pace

## Challenges
- Requires cultural shift
- May be difficult to implement in traditional organizations
- Requires discipline and commitment
- May be challenging to measure benefits initially
- Requires leadership support
"""

    def _get_prince2_knowledge(self) -> str:
        """Get knowledge about PRINCE2 methodology.

        Returns:
            Knowledge about PRINCE2 methodology.
        """
        return """
# PRINCE2 Project Management Methodology

## Core Principles
- Continued business justification
- Learn from experience
- Defined roles and responsibilities
- Manage by stages
- Manage by exception
- Focus on products
- Tailor to suit the project environment

## Key Processes
1. Starting up a Project
2. Directing a Project
3. Initiating a Project
4. Controlling a Stage
5. Managing Product Delivery
6. Managing Stage Boundaries
7. Closing a Project

## Roles
- Project Board
  - Executive
  - Senior User
  - Senior Supplier
- Project Manager
- Team Manager
- Project Assurance
- Project Support
- Change Authority

## Themes
- Business Case
- Organization
- Quality
- Plans
- Risk
- Change
- Progress

## Benefits
- Established best practices
- Clearly defined roles and responsibilities
- Controlled start, middle, and end
- Regular reviews of progress against plan
- Flexible decision points
- Automatic control of deviations
- Stakeholder involvement at the right times

## Challenges
- Can be bureaucratic if not tailored properly
- Requires training and certification
- May be perceived as document-heavy
- Less flexible than agile approaches
- May be overkill for small projects
"""

    def _get_pmi_knowledge(self) -> str:
        """Get knowledge about PMI/PMBOK methodology.

        Returns:
            Knowledge about PMI/PMBOK methodology.
        """
        return """
# PMI/PMBOK Project Management Methodology

## Core Knowledge Areas
1. Integration Management
2. Scope Management
3. Schedule Management
4. Cost Management
5. Quality Management
6. Resource Management
7. Communications Management
8. Risk Management
9. Procurement Management
10. Stakeholder Management

## Process Groups
1. Initiating
2. Planning
3. Executing
4. Monitoring and Controlling
5. Closing

## Key Documents
- Project Charter
- Project Management Plan
- Requirements Documentation
- Work Breakdown Structure (WBS)
- Schedule
- Budget
- Risk Register
- Stakeholder Register
- Communications Plan
- Quality Management Plan

## Tools and Techniques
- Expert Judgment
- Data Analysis
- Meetings
- Interpersonal and Team Skills
- PMIS (Project Management Information System)
- Earned Value Management
- Critical Path Method
- Resource Leveling
- Risk Analysis

## Benefits
- Comprehensive framework
- Globally recognized standard
- Adaptable to various industries
- Clear processes and documentation
- Strong focus on stakeholder management
- Emphasis on integration across knowledge areas

## Challenges
- Can be perceived as document-heavy
- May require significant planning effort
- Less adaptive than agile approaches
- Requires experienced project managers
- May be overkill for small projects
"""

    def _get_hybrid_knowledge(self) -> str:
        """Get knowledge about Hybrid methodology.

        Returns:
            Knowledge about Hybrid methodology.
        """
        return """
# Hybrid Project Management Methodology

## Core Principles
- Combine the best of traditional and agile approaches
- Adapt methodology to project needs
- Balance predictability with flexibility
- Focus on value delivery
- Continuous improvement
- Stakeholder engagement

## Common Hybrid Approaches
- Agile-Waterfall Hybrid
- Scrumban (Scrum + Kanban)
- Water-Scrum-Fall
- Disciplined Agile Delivery (DAD)
- Scaled Agile Framework (SAFe)

## Key Practices
- Upfront planning for the overall project
- Iterative development within phases
- Regular stakeholder reviews
- Flexible scope within fixed constraints
- Risk-based approach to methodology selection
- Tailored documentation

## When to Use Hybrid
- Complex projects with both predictable and unpredictable elements
- Projects with regulatory or compliance requirements
- Organizations transitioning from traditional to agile
- Projects with diverse teams and skill sets
- Projects with mixed delivery requirements

## Benefits
- Combines strengths of multiple methodologies
- Adaptable to organizational constraints
- Balances flexibility and stability
- Accommodates diverse stakeholder needs
- Provides structure while allowing for change
- Easier transition for traditional organizations

## Challenges
- Requires experienced project managers
- May create confusion about processes
- Requires clear communication about methodology
- May be difficult to implement consistently
- Requires careful tailoring to project needs
"""
