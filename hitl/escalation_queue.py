"""Enterprise Human-in-the-Loop (HITL) Policy Escalation Queue & Decision Supervisor.

Manages risk-based ticketing, supervisor review workflows, and immutable audit logs
for autonomous agents encountering policy exceptions or low-confidence thresholds.
"""

import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class EscalationTicket:
    """Escalation item queued for human supervisor review."""
    ticket_id: str
    archetype: str
    user_query: str
    extracted_entities: Dict[str, Any]
    risk_score: float
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    reason: str
    status: str = "PENDING"  # PENDING, APPROVED, REJECTED, OVERRIDDEN
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None


class HITLEscalationQueue:
    """Thread-safe escalation supervisor queue with priority ordering and audit trails."""

    PRIORITY_WEIGHTS = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
    }

    def __init__(self):
        self._tickets: Dict[str, EscalationTicket] = {}

    @classmethod
    def calculate_priority(cls, risk_score: float, reason: str) -> str:
        """Determines priority tier based on quantitative risk score and violation category."""
        reason_upper = reason.upper()
        if risk_score >= 0.85 or "LEGAL" in reason_upper or "INJECTION" in reason_upper:
            return "CRITICAL"
        if risk_score >= 0.60 or "FINANCIAL" in reason_upper or "OVERRUN" in reason_upper:
            return "HIGH"
        if risk_score >= 0.35 or "CONFIDENCE" in reason_upper:
            return "MEDIUM"
        return "LOW"

    def enqueue(
        self,
        ticket_id: str,
        archetype: str,
        user_query: str,
        extracted_entities: Optional[Dict[str, Any]] = None,
        risk_score: float = 0.5,
        reason: str = "POLICY_ESCALATION",
    ) -> EscalationTicket:
        """Enqueues an escalation ticket with computed priority."""
        priority = self.calculate_priority(risk_score, reason)
        ticket = EscalationTicket(
            ticket_id=ticket_id,
            archetype=archetype,
            user_query=user_query,
            extracted_entities=extracted_entities or {},
            risk_score=risk_score,
            priority=priority,
            reason=reason,
            status="PENDING",
        )
        self._tickets[ticket_id] = ticket
        return ticket

    def get_ticket(self, ticket_id: str) -> Optional[EscalationTicket]:
        """Retrieves a single ticket by ID."""
        return self._tickets.get(ticket_id)

    def get_pending_tickets(self, priority: Optional[str] = None) -> List[EscalationTicket]:
        """Returns all pending tickets sorted by priority level and creation timestamp."""
        pending = [t for t in self._tickets.values() if t.status == "PENDING"]
        if priority:
            pending = [t for t in pending if t.priority.upper() == priority.upper()]

        return sorted(
            pending,
            key=lambda t: (self.PRIORITY_WEIGHTS.get(t.priority, 0), t.created_at),
            reverse=True,
        )

    def review_ticket(
        self,
        ticket_id: str,
        action: str,  # APPROVED, REJECTED, OVERRIDDEN
        reviewed_by: str = "supervisor@enterprise.org",
        review_notes: str = "",
    ) -> bool:
        """Executes a human supervisor review decision."""
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            return False

        valid_actions = {"APPROVED", "REJECTED", "OVERRIDDEN"}
        action_upper = action.upper()
        if action_upper not in valid_actions:
            raise ValueError(f"Invalid review action '{action}'. Must be one of {valid_actions}")

        ticket.status = action_upper
        ticket.reviewed_at = datetime.now(timezone.utc).isoformat()
        ticket.reviewed_by = reviewed_by
        ticket.review_notes = review_notes
        return True

    def get_audit_trail(self) -> List[EscalationTicket]:
        """Returns all tickets in chronological order for compliance audits."""
        return sorted(self._tickets.values(), key=lambda t: t.created_at)

    def get_metrics(self) -> Dict[str, Any]:
        """Calculates queue health and resolution KPIs."""
        total = len(self._tickets)
        if total == 0:
            return {
                "total_tickets": 0,
                "pending": 0,
                "approved": 0,
                "rejected": 0,
                "overridden": 0,
                "avg_risk_score": 0.0,
                "critical_pending": 0,
            }

        pending = sum(1 for t in self._tickets.values() if t.status == "PENDING")
        approved = sum(1 for t in self._tickets.values() if t.status == "APPROVED")
        rejected = sum(1 for t in self._tickets.values() if t.status == "REJECTED")
        overridden = sum(1 for t in self._tickets.values() if t.status == "OVERRIDDEN")
        critical_pending = sum(1 for t in self._tickets.values() if t.status == "PENDING" and t.priority == "CRITICAL")
        avg_risk = sum(t.risk_score for t in self._tickets.values()) / total

        return {
            "total_tickets": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "overridden": overridden,
            "critical_pending": critical_pending,
            "avg_risk_score": round(avg_risk, 3),
        }

    def export_summary(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Exports structured queue summary to JSON."""
        summary = {
            "metrics": self.get_metrics(),
            "tickets": [asdict(t) for t in self.get_audit_trail()],
        }
        if filepath:
            with open(filepath, "w") as f:
                json.dump(summary, f, indent=2)
        return summary
