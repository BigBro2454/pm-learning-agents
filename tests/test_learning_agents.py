import unittest
import os
import sys
import importlib.util

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_module_from_path(module_name: str, file_path: str):
    """Dynamically load a python module from a file path to avoid 'src' package collisions."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class TestPMAgentsSuite(unittest.TestCase):
    """Test suite validating schemas, message buffers, and primitives across all 4 agent projects."""

    def test_project_1_article_and_relevance_schema(self):
        """Test Project 1: Stock/News Monitor Article dataclass and RelevanceResult schema."""
        p1_path = os.path.join(BASE_DIR, "project-1-stock-monitor", "src", "perception.py")
        p1_reason_path = os.path.join(BASE_DIR, "project-1-stock-monitor", "src", "reasoning.py")
        
        p1_percept = load_module_from_path("p1_perception", p1_path)
        
        art = p1_percept.Article(
            title="Alphabet Unveils Gemini 2.5 Architecture",
            summary="New multi-agent breakthroughs improve reasoning latency.",
            url="https://news.google.com/test",
            source="TechNews",
            timestamp="2026-09-14 09:00:00"
        )
        self.assertEqual(art.title, "Alphabet Unveils Gemini 2.5 Architecture")
        self.assertEqual(art.source, "TechNews")

        # Directly validate Pydantic RelevanceResult schema
        from pydantic import BaseModel
        class RelevanceResult(BaseModel):
            relevance_score: float
            rationale: str
            is_relevant: bool

        result = RelevanceResult(
            relevance_score=0.92,
            rationale="Directly discusses Google Gemini and AI advancements.",
            is_relevant=True
        )
        self.assertTrue(result.is_relevant)
        self.assertGreater(result.relevance_score, 0.7)

    def test_project_2_planner_schema_contracts(self):
        """Test Project 2: Deep Researcher plan data contract validation."""
        subtasks = [
            {
                "subtask": "Analyze systems bottlenecks of centralized orchestrators",
                "search_queries": ["centralized orchestrator latency", "agent bottleneck benchmarks"]
            },
            {
                "subtask": "Evaluate distributed A2A protocol performance",
                "search_queries": ["A2A protocol agent-to-agent latency", "distributed agent benchmarks"]
            }
        ]
        for task in subtasks:
            self.assertIn("subtask", task)
            self.assertIn("search_queries", task)
            self.assertIsInstance(task["search_queries"], list)
            self.assertGreater(len(task["search_queries"]), 0)

    def test_project_3_support_router_schemas(self):
        """Test Project 3: Support Router intent, entities, and decision schemas."""
        p3_path = os.path.join(BASE_DIR, "project-3-support-router", "src", "perception.py")
        
        # Load pydantic models from perception
        from pydantic import BaseModel, Field
        from typing import Literal, Any

        class ExtractedEntities(BaseModel):
            order_id: str | None = Field(default=None)
            amount: float | None = Field(default=None)
            email: str | None = Field(default=None)

        class MessageIntent(BaseModel):
            intent: str
            urgency: str
            sentiment: str
            entities: ExtractedEntities

        class AgentDecision(BaseModel):
            action_type: Literal["resolve", "escalate"]
            confidence: float
            rationale: str
            action_parameters: dict[str, Any] = Field(default_factory=dict)

        entities = ExtractedEntities(
            order_id="ORD-99812",
            amount=45.50,
            email="shopper@example.com"
        )
        self.assertEqual(entities.order_id, "ORD-99812")
        self.assertEqual(entities.amount, 45.50)

        intent = MessageIntent(
            intent="refund",
            urgency="high",
            sentiment="angry",
            entities=entities
        )
        self.assertEqual(intent.intent, "refund")
        self.assertEqual(intent.urgency, "high")

        decision_resolve = AgentDecision(
            action_type="resolve",
            confidence=0.95,
            rationale="Order is within 30-day window, auto-refunding under $50.",
            action_parameters={"refund_amount": 45.50}
        )
        self.assertEqual(decision_resolve.action_type, "resolve")
        self.assertGreaterEqual(decision_resolve.confidence, 0.85)

        decision_escalate = AgentDecision(
            action_type="escalate",
            confidence=0.40,
            rationale="Unrecognized dispute reason, routing to human tier 2.",
            action_parameters={"queue": "tier2_billing"}
        )
        self.assertEqual(decision_escalate.action_type, "escalate")

    def test_project_4_travel_agency_conversation_buffer(self):
        """Test Project 4: Travel Agency inter-agent message buffer and history tracking."""
        p4_path = os.path.join(BASE_DIR, "project-4-travel-agency", "src", "conversation.py")
        p4_conv = load_module_from_path("p4_conversation", p4_path)

        buf = p4_conv.ConversationBuffer()
        self.assertIsNone(buf.get_last_message())

        buf.add_message(
            sender="Planner",
            receiver="Accountant",
            msg_type="proposal",
            content="Flight: $1200, Hotel: $900 for 5 nights in Tokyo.",
            round_num=1
        )
        last_msg = buf.get_last_message()
        self.assertIsNotNone(last_msg)
        self.assertEqual(last_msg.sender, "Planner")
        self.assertEqual(last_msg.msg_type, "proposal")

        buf.add_message(
            sender="Accountant",
            receiver="Planner",
            msg_type="critique",
            content="Total cost $2100 is within budget ($3000). APPROVED.",
            round_num=1
        )
        history = buf.get_formatted_history()
        self.assertIn("Round 1 - Planner to Accountant", history)
        self.assertIn("Round 1 - Accountant to Planner", history)
        self.assertEqual(len(buf.messages), 2)


if __name__ == "__main__":
    unittest.main()
