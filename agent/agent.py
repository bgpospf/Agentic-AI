"""
Basic agent foundation.

This module will eventually:
1. Receive a user task
2. Create an execution plan
3. Select tools
4. Execute tools
5. Record the trajectory
6. Return a final response
"""

from datetime import datetime


class Agent:
    """Basic foundation for the Agentic-AI evaluation project."""

    def __init__(self):
        self.trajectory = []

    def record_step(self, step_type, data):
        """Record one step in the agent trajectory."""

        self.trajectory.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "step_type": step_type,
                "data": data,
            }
        )

    def run(self, user_task):
        """Run the agent for a user task."""

        self.record_step(
            "intent",
            {
                "user_task": user_task
            }
        )

        # Planning will be added next.
        self.record_step(
            "plan",
            {
                "status": "not_implemented"
            }
        )

        return {
            "status": "success",
            "message": "Agent foundation created.",
            "trajectory": self.trajectory,
        }


if __name__ == "__main__":
    agent = Agent()

    result = agent.run(
        "Why can't my private EC2 communicate with my VPN client?"
    )

    print(result)
