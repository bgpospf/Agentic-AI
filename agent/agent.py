"""
Agentic AI Evaluation Harness
=============================

This module defines the core Agent class for the Agentic-AI
project.

The project is designed to build and evaluate production-oriented
AI agents that can work with AWS infrastructure, tools, RAG,
safety controls, observability, and evaluation systems.

Agent workflow
--------------

    User Request
        |
        v
      Intent
        |
        v
      Plan
        |
        v
     Retrieve
        |
        v
   Tool Selection
        |
        v
   Tool Execution
        |
        v
     Validate
        |
        +-------> Recover
        |             |
        |             v
        +--------> Re-execute
        |
        v
     Respond
        |
        v
    Trajectory
        |
        v
   Evaluation


Current implementation
----------------------

The first implementation intentionally starts with a READ-only
AWS VPC operation.

Current AWS tool:

    describe_vpcs()

Future capabilities will include:

    AWS Networking
        - VPC
        - Subnets
        - Route Tables
        - EC2
        - Internet Gateway
        - NAT Gateway
        - Transit Gateway
        - Cloud WAN
        - Global Network

    Agent capabilities
        - Planning
        - Tool selection
        - Tool execution
        - Validation
        - Recovery
        - Safety
        - Human approval
        - Observability
        - Evaluation

    AI capabilities
        - LLM reasoning
        - RAG
        - Grounded responses
        - Prompt-injection testing
        - LLM-as-a-judge
        - Human evaluation

    Evaluation
        - Golden datasets
        - Adversarial datasets
        - Regression datasets
        - Offline evaluation
        - Online monitoring
        - Trajectory evaluation


Risk model
----------

Tools will eventually be classified into:

    READ
        Safe inspection operations.

    WRITE
        Infrastructure-changing operations.

    HIGH_RISK
        Destructive or highly sensitive operations.

Write and high-risk actions will require additional controls
such as authorization, validation, policy checks, and human
approval.


Trajectory
----------

Every important agent step is recorded.

The trajectory will eventually contain:

    intent
    plan
    retrieve
    tool_selection
    tool_execution
    validation
    recovery
    response

This allows evaluation of the agent's process, not only its
final answer.

The evaluation system will later measure:

    - Outcome quality
    - Process / trajectory quality
    - Reliability and consistency
    - Safety
    - Efficiency
    - Tool usage
    - Scope discipline
    - Recovery behavior
"""


from datetime import datetime

from tools.aws_vpc import describe_vpcs


class Agent:
    """
    Core Agent controller.

    This class is responsible for coordinating the agent
    workflow.

    The class is intentionally separated from individual tools.

    Agent
        |
        +-- Planning
        +-- Retrieval
        +-- Tool Selection
        +-- Tool Execution
        +-- Validation
        +-- Recovery
        +-- Response
        |
        +-- Trajectory

    Individual AWS tools live separately under:

        agent/tools/
    """

    def __init__(self, region="us-east-1"):
        """
        Initialize the agent.

        Parameters
        ----------
        region : str
            AWS region used by the agent.

        Attributes
        ----------
        region : str
            AWS region.

        trajectory : list
            Complete record of the current agent execution.
        """

        self.region = region

        # Stores every important execution step.
        self.trajectory = []

        # Current execution state.
        self.state = "initialized"

    # ======================================================
    # TRAJECTORY
    # ======================================================

    def record_step(self, step_type, data):
        """
        Record an agent execution step.

        Parameters
        ----------
        step_type : str
            Type of execution step.

        data : dict
            Information associated with the step.
        """

        self.trajectory.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "step_type": step_type,
                "data": data,
            }
        )

    # ======================================================
    # INTENT
    # ======================================================

    def understand_intent(self, user_task):
        """
        Understand the user's requested task.

        Current version:
            Records the task directly.

        Future version:
            The LLM will interpret the request and extract
            intent, entities, constraints, and desired outcome.
        """

        self.state = "intent"

        intent = {
            "user_task": user_task,
            "status": "identified",
        }

        self.record_step(
            "intent",
            intent,
        )

        return intent

    # ======================================================
    # PLAN
    # ======================================================

    def create_plan(self, intent):
        """
        Create an execution plan.

        Current version:
            Creates a simple inspection plan.

        Future version:
            The LLM will generate a structured plan based on
            the user's intent, available tools, policies,
            knowledge, and infrastructure state.
        """

        self.state = "planning"

        plan = {
            "steps": [
                "inspect AWS VPC infrastructure",
                "collect VPC information",
                "validate results",
                "prepare response",
            ],
            "status": "created",
        }

        self.record_step(
            "plan",
            plan,
        )

        return plan

    # ======================================================
    # RETRIEVAL
    # ======================================================

    def retrieve_context(self, intent):
        """
        Retrieve relevant context for the task.

        Current version:
            No external retrieval is required.

        Future version:
            This method can connect to RAG and retrieve:

                - AWS documentation
                - Network documentation
                - Customer configuration
                - Architecture knowledge
                - Policies
                - Runbooks
                - Previous incidents
        """

        self.state = "retrieval"

        context = {
            "status": "not_required",
            "sources": [],
        }

        self.record_step(
            "retrieve",
            context,
        )

        return context

    # ======================================================
    # TOOL SELECTION
    # ======================================================

    def select_tool(self, plan):
        """
        Select the appropriate tool for the current plan.

        Current version:
            Uses the read-only describe_vpcs tool.

        Future version:
            The LLM/tool router will select from a registered
            tool catalog.
        """

        self.state = "tool_selection"

        tool = {
            "name": "describe_vpcs",
            "operation_type": "READ",
            "approval_required": False,
        }

        self.record_step(
            "tool_selection",
            tool,
        )

        return tool

    # ======================================================
    # TOOL EXECUTION
    # ======================================================

    def execute_tool(self, tool):
        """
        Execute the selected tool.

        Current implementation supports:

            describe_vpcs

        Future versions will support additional AWS,
        networking, Kubernetes, automation, and RAG tools.
        """

        self.state = "tool_execution"

        if tool["name"] == "describe_vpcs":

            result = describe_vpcs(
                self.region
            )

        else:

            raise ValueError(
                f"Unsupported tool: {tool['name']}"
            )

        self.record_step(
            "tool_execution",
            {
                "tool": tool["name"],
                "operation_type": tool["operation_type"],
                "result_count": len(result),
            },
        )

        return result

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate(self, result):
        """
        Validate the result returned by the tool.

        Current version:
            Performs basic result validation.

        Future version:
            Validation will include:

                - Schema validation
                - Policy validation
                - Expected state
                - Safety checks
                - Grounding checks
                - Infrastructure consistency
        """

        self.state = "validation"

        valid = isinstance(result, list)

        validation = {
            "valid": valid,
            "status": "passed" if valid else "failed",
        }

        self.record_step(
            "validation",
            validation,
        )

        return validation

    # ======================================================
    # RECOVERY
    # ======================================================

    def recover(self, error):
        """
        Recover from an execution failure.

        Current version:
            Records the failure.

        Future version:
            Recovery can include:

                - Retry
                - Alternative tool
                - Revised plan
                - Additional retrieval
                - Human escalation
                - Safe termination
        """

        self.state = "recovery"

        recovery = {
            "status": "recorded",
            "error": str(error),
        }

        self.record_step(
            "recovery",
            recovery,
        )

        return recovery

    # ======================================================
    # RESPONSE
    # ======================================================

    def generate_response(self, result):
        """
        Generate the final response.

        Current version:
            Returns a simple structured response.

        Future version:
            The LLM will generate a grounded response using
            validated tool results and retrieved context.
        """

        self.state = "response"

        response = {
            "message": f"Found {len(result)} VPC(s).",
            "vpc_count": len(result),
        }

        self.record_step(
            "response",
            response,
        )

        return response

    # ======================================================
    # MAIN AGENT LOOP
    # ======================================================

    def run(self, user_task):
        """
        Run the complete agent workflow.

        Workflow:

            Intent
              ↓
            Plan
              ↓
            Retrieve
              ↓
            Tool Selection
              ↓
            Tool Execution
              ↓
            Validation
              ↓
            Response

        If execution fails, the recovery stage is invoked.
        """

        self.trajectory = []
        self.state = "running"

        try:

            # 1. Understand user intent
            intent = self.understand_intent(
                user_task
            )

            # 2. Create execution plan
            plan = self.create_plan(
                intent
            )

            # 3. Retrieve supporting context
            self.retrieve_context(
                intent
            )

            # 4. Select tool
            tool = self.select_tool(
                plan
            )

            # 5. Execute tool
            result = self.execute_tool(
                tool
            )

            # 6. Validate result
            validation = self.validate(
                result
            )

            if not validation["valid"]:

                raise ValueError(
                    "Tool result validation failed."
                )

            # 7. Generate response
            response = self.generate_response(
                result
            )

            self.state = "completed"

            return {
                "status": "success",
                "state": self.state,
                "response": response,
                "data": result,
                "trajectory": self.trajectory,
            }

        except Exception as error:

            self.recover(
                error
            )

            self.state = "failed"

            return {
                "status": "failed",
                "state": self.state,
                "error": str(error),
                "trajectory": self.trajectory,
            }


# ==========================================================
# LOCAL TEST
# ==========================================================

if __name__ == "__main__":

    agent = Agent(
        region="us-east-1"
    )

    result = agent.run(
        "Show me the VPCs in my AWS account."
    )

    print("\n=== AGENT RESULT ===")
    print(result)

    print("\n=== AGENT TRAJECTORY ===")

    for step in result["trajectory"]:
        print(step)
