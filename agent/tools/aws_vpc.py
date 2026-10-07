"""
Basic Agentic AI foundation.

The agent receives a task, selects an AWS read-only tool,
executes it, and records the trajectory.
"""

from datetime import datetime

from tools.aws_vpc import describe_vpcs


class Agent:
    """Basic agent with AWS read-only tool access."""

    def __init__(self, region="us-east-1"):
        self.region = region
        self.trajectory = []

    def record_step(self, step_type, data):
        """Record an agent execution step."""

        self.trajectory.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "step_type": step_type,
                "data": data,
            }
        )

    def run(self, user_task):
        """Run the agent for a user task."""

        # 1. Record user intent
        self.record_step(
            "intent",
            {
                "user_task": user_task
            }
        )

        # 2. Select a READ-only AWS tool
        self.record_step(
            "tool_selection",
            {
                "tool": "describe_vpcs",
                "risk": "READ"
            }
        )

        # 3. Execute the AWS tool
        vpcs = describe_vpcs(self.region)

        self.record_step(
            "tool_execution",
            {
                "tool": "describe_vpcs",
                "result_count": len(vpcs)
            }
        )

        # 4. Return the result
        return {
            "status": "success",
            "vpcs": vpcs,
            "trajectory": self.trajectory,
        }


if __name__ == "__main__":

    agent = Agent(
        region="us-east-1"
    )

    result = agent.run(
        "Show me the VPCs in my AWS account."
    )

    print(result)
