"""Enterprise Security Guardrails & Policy Defense-in-Depth Engine.

Implements zero-token, sub-millisecond deterministic defense across:
  1. Adversarial Prompt Injection & Jailbreak Neutralization
  2. PCI-DSS & GDPR PII Redaction (Credit Cards, SSNs, Phone, Email)
  3. Programmatic Financial Ceiling Enforcement
  4. Legal & Hostile Escalation Boundary Interception
"""

import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class GuardrailResult:
    """Quantitative validation outcome for input/output payloads."""
    passed: bool
    action: str  # ALLOW, SANITIZE, ESCALATE, BLOCK
    original_text: str
    sanitized_text: str
    violations: List[str] = field(default_factory=list)
    pii_detected: Dict[str, int] = field(default_factory=dict)
    latency_ms: float = 0.0
    reason: Optional[str] = None


class AgentGuardrails:
    """Defense-in-depth safety engine for applied autonomous agent archetypes."""

    # 1. Adversarial Prompt Injection Signatures
    INJECTION_PATTERNS = [
        (re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?", re.IGNORECASE), "PROMPT_INJECTION_IGNORE_DIRECTIVES"),
        (re.compile(r"disregard\s+(?:all\s+)?(?:previous|prior)\s+rules?", re.IGNORECASE), "PROMPT_INJECTION_DISREGARD_RULES"),
        (re.compile(r"system\s+prompt\s+override", re.IGNORECASE), "PROMPT_INJECTION_SYSTEM_OVERRIDE"),
        (re.compile(r"(?:reveal|print|show|dump)\s+(?:your\s+)?(?:system|initial|hidden)?\s*(?:prompts?|instructions?)", re.IGNORECASE), "SYSTEM_PROMPT_EXTRACTION"),
        (re.compile(r"you\s+are\s+now\s+(?:in\s+)?(?:dan|developer|jailbreak|unrestricted)\s+mode", re.IGNORECASE), "JAILBREAK_ROLEPLAY"),
        (re.compile(r"do\s+anything\s+now", re.IGNORECASE), "JAILBREAK_DAN_DIRECTIVE"),
        (re.compile(r"</?instruction>|---BEGIN\s+SYSTEM\s+INSTRUCTION---", re.IGNORECASE), "DELIMITER_HIJACKING"),
    ]

    # 2. PII Regex Patterns
    PII_PATTERNS = {
        "credit_card": re.compile(r"\b(?:\d{4}[- ]?){3}\d{4}\b"),
        "ssn": re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"),
        "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone": re.compile(r"\b(?:\+?1[-. ]?)?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b"),
    }

    # 3. Hostile Sentiment & Legal Threat Keywords
    LEGAL_THREAT_PATTERNS = [
        re.compile(r"\b(?:my\s+)?(?:lawyer|attorney|legal\s+counsel)\b", re.IGNORECASE),
        re.compile(r"\b(?:sue\s+you|filing\s+a\s+lawsuit|take\s+you\s+to\s+court)\b", re.IGNORECASE),
        re.compile(r"\b(?:better\s+business\s+bureau|regulatory\s+complaint|cfpb|arbitration)\b", re.IGNORECASE),
        re.compile(r"\b(?:class\s+action\s+lawsuit)\b", re.IGNORECASE),
    ]

    def __init__(self, default_financial_limit: float = 500.0):
        self.default_financial_limit = default_financial_limit

    def inspect(self, text: str, financial_amount: Optional[float] = None) -> GuardrailResult:
        """Inspects text payload through multi-tier deterministic security filters."""
        start_time = time.perf_counter()
        violations = []
        pii_counts = {}
        sanitized = text
        action = "ALLOW"
        reason = None

        # Tier 1: Check for Adversarial Prompt Injection (Hard Block)
        for pattern, violation_code in self.INJECTION_PATTERNS:
            if pattern.search(text):
                violations.append(violation_code)

        if violations:
            action = "BLOCK"
            reason = f"Adversarial prompt injection detected: {', '.join(violations)}"
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            return GuardrailResult(
                passed=False,
                action=action,
                original_text=text,
                sanitized_text=sanitized,
                violations=violations,
                pii_detected=pii_counts,
                latency_ms=round(latency_ms, 3),
                reason=reason,
            )

        # Tier 2: Check for Legal & Regulatory Threats (Escalate to HITL)
        for pattern in self.LEGAL_THREAT_PATTERNS:
            if pattern.search(text):
                violations.append("LEGAL_ESCALATION_REQUIRED")
                action = "ESCALATE"
                reason = "Legal counsel or regulatory complaint detected; escalating to Tier-2 supervisor."
                break

        # Tier 3: Financial Boundary Enforcement
        if financial_amount is not None and financial_amount > self.default_financial_limit:
            violations.append(f"FINANCIAL_LIMIT_EXCEEDED (${financial_amount:.2f} > ${self.default_financial_limit:.2f})")
            action = "ESCALATE"
            reason = f"Transaction amount ${financial_amount:.2f} exceeds auto-approval threshold ${self.default_financial_limit:.2f}."

        # Tier 4: PII Redaction & Sanitization
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = pattern.findall(sanitized)
            if matches:
                pii_counts[pii_type] = len(matches)
                sanitized = pattern.sub(f"[REDACTED_{pii_type.upper()}]", sanitized)

        if pii_counts and action == "ALLOW":
            action = "SANITIZE"

        passed = action in ("ALLOW", "SANITIZE")
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return GuardrailResult(
            passed=passed,
            action=action,
            original_text=text,
            sanitized_text=sanitized,
            violations=violations,
            pii_detected=pii_counts,
            latency_ms=round(latency_ms, 3),
            reason=reason,
        )

    def mask_pii(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Convenience method to strictly redact PII from any payload."""
        sanitized = text
        pii_counts = {}
        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = pattern.findall(sanitized)
            if matches:
                pii_counts[pii_type] = len(matches)
                sanitized = pattern.sub(f"[REDACTED_{pii_type.upper()}]", sanitized)
        return sanitized, pii_counts

    def validate_budget_constraint(self, amount: float, ceiling: float) -> Tuple[bool, Optional[str]]:
        """Validates travel or operational budget against a strict financial ceiling."""
        if amount > ceiling:
            return False, f"Budget overrun: proposed amount ${amount:.2f} exceeds ceiling ${ceiling:.2f}"
        return True, None
