"""Unit & Integration Test Suite for Enterprise Guardrails, Vertex AI Economics & Fleet Governance.

Phase 3 / Feature PR #3 (Day 37)

Validates:
  1. Outbound credential leak suppression (Gemini, OpenAI, Anthropic, GitHub, AWS, Bearer).
  2. TokenBucketRateLimiter burst capacity, consumption, exhaustion, and multi-client isolation.
  3. Integrated rate limiting inside AgentGuardrails.inspect().
  4. EnterpriseModelBenchmarker pricing formulas, 50% prompt caching discount, and >97% cost reduction.
  5. JSON & Markdown report generation for Enterprise Token Economics.
  6. FleetGovernanceAuditor 4-archetype audit matrix, Grade A+ readiness, and SLA benchmarks.
  7. JSON & Markdown report generation for Fleet Governance Matrix.
"""

import json
import os
import tempfile
import time
import unittest

from guardrails.agent_guardrails import AgentGuardrails, GuardrailResult, TokenBucketRateLimiter
from telemetry.enterprise_benchmarks import (
    ARCHETYPE_WORKLOADS,
    PRICING_CATALOG,
    EnterpriseModelBenchmarker,
    enterprise_benchmarker,
)
from telemetry.fleet_governance import (
    GOVERNANCE_CATALOG,
    FleetGovernanceAuditor,
    fleet_governance,
)


class TestEnterpriseGuardrailsGovernance(unittest.TestCase):
    """Test suite for Phase 3 enterprise deliverables."""

    def setUp(self):
        self.guardrails = AgentGuardrails(default_financial_limit=500.0)
        self.benchmarker = EnterpriseModelBenchmarker()
        self.governance = FleetGovernanceAuditor()

    # ── 1. CREDENTIAL LEAK SUPPRESSION TESTS ──────────────────────────────────

    def test_credential_leak_suppression(self):
        """Verify egress redaction across all enterprise credential signatures."""
        test_cases = [
            ("Deploy with GEMINI=AIzaSyA1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6 now.", "GOOGLE_API_KEY"),
            ("Set key sk-1234567890123456789012345678901234 in header.", "GENERIC_API_KEY"),
            ("Use token sk-ant-api03-abcdef1234567890abcdef1234567890 for Claude.", "ANTHROPIC_API_KEY"),
            ("Push with ghp_123456789012345678901234567890123456 to repo.", "GITHUB_TOKEN"),
            ("AWS bucket key AKIAIOSFODNN7EXAMPLE used.", "AWS_ACCESS_KEY"),
            ("Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xyz", "BEARER_TOKEN"),
        ]

        for text, cred_type in test_cases:
            sanitized, redacted = self.guardrails.redact_credentials(text)
            self.assertIn(cred_type, redacted, f"Failed to identify credential type {cred_type}")
            self.assertIn(f"[REDACTED_{cred_type}]", sanitized)

    def test_inspect_with_credential_leak(self):
        """Verify inspect() marks credential leaks as SANITIZE and records violation."""
        text = "Contact lead at user@enterprise.com with API key AIzaSyD3m0K3yV4l1dP4ssw0rd123456789012."
        res = self.guardrails.inspect(text)
        self.assertTrue(res.passed)
        self.assertEqual(res.action, "SANITIZE")
        self.assertTrue(any("CREDENTIAL_LEAK_SUPPRESSED" in v for v in res.violations))
        self.assertIn("[REDACTED_GOOGLE_API_KEY]", res.sanitized_text)
        self.assertIn("[REDACTED_EMAIL]", res.sanitized_text)

    # ── 2. TOKEN BUCKET RATE LIMITER TESTS ────────────────────────────────────

    def test_rate_limiter_burst_and_exhaustion(self):
        """Verify rate limiter allows burst up to capacity and blocks upon exhaustion."""
        limiter = TokenBucketRateLimiter(capacity=5.0, refill_rate=1.0)

        # Consume 5 tokens immediately
        for _ in range(5):
            self.assertTrue(limiter.consume("client-1", tokens=1.0))

        # 6th should fail
        self.assertFalse(limiter.consume("client-1", tokens=1.0))

        # Other client has its own fresh bucket
        self.assertTrue(limiter.consume("client-2", tokens=1.0))

    def test_rate_limiter_refill_and_reset(self):
        """Verify token bucket refills over time and responds to reset."""
        limiter = TokenBucketRateLimiter(capacity=3.0, refill_rate=10.0)
        self.assertTrue(limiter.consume("client-1", tokens=3.0))
        self.assertFalse(limiter.consume("client-1", tokens=1.0))

        # Wait for refill
        time.sleep(0.15)
        self.assertTrue(limiter.consume("client-1", tokens=1.0))

        # Reset clears state
        limiter.reset("client-1")
        self.assertEqual(limiter.get_available_tokens("client-1"), 3.0)

    def test_inspect_rate_limit_integration(self):
        """Verify inspect() enforces rate limiting when enabled."""
        small_limiter = TokenBucketRateLimiter(capacity=1.0, refill_rate=0.1)
        guard = AgentGuardrails(rate_limiter=small_limiter)

        # 1st call passes
        res1 = guard.inspect("Normal query 1", client_id="user-a", enforce_rate_limit=True)
        self.assertTrue(res1.passed)

        # 2nd call is rate-limited
        res2 = guard.inspect("Normal query 2", client_id="user-a", enforce_rate_limit=True)
        self.assertFalse(res2.passed)
        self.assertEqual(res2.action, "BLOCK")
        self.assertIn("RATE_LIMIT_EXCEEDED", res2.violations)

    # ── 3. ENTERPRISE TOKEN ECONOMICS BENCHMARK TESTS ─────────────────────────

    def test_enterprise_benchmarks_totals(self):
        """Verify total token calculations across 4 archetypes."""
        toks = self.benchmarker.total_tokens()
        self.assertEqual(len(self.benchmarker.workloads), 4)
        self.assertEqual(toks["total_input"], 240 + 950 + 480 + 820)
        self.assertEqual(toks["total_output"], 80 + 420 + 160 + 390)
        self.assertEqual(toks["total_cacheable"], 120 + 480 + 240 + 410)
        self.assertEqual(toks["total_tokens"], toks["total_input"] + toks["total_output"])

    def test_pricing_and_prompt_caching_discount(self):
        """Verify Gemini 2.5 Flash prompt caching yields measurable savings."""
        base_cost = self.benchmarker.compute_single_run_cost("gemini-2.5-flash", use_prompt_caching=False)
        cached_cost = self.benchmarker.compute_single_run_cost("gemini-2.5-flash", use_prompt_caching=True, cache_ratio=0.5)

        self.assertGreater(base_cost, cached_cost)
        self.assertAlmostEqual(
            base_cost - cached_cost,
            (self.benchmarker.total_tokens()["total_input"] * 0.5 / 1e6) * (0.075 - 0.0375),
            places=6,
        )

    def test_cross_model_savings_projections(self):
        """Verify Gemini 2.5 Flash achieves >97% enterprise cost reduction vs GPT-4o and Claude."""
        savings_gpt = self.benchmarker.calculate_savings(500_000, "gpt-4o", "gemini-2.5-flash", True)
        savings_claude = self.benchmarker.calculate_savings(500_000, "claude-3-5-sonnet", "gemini-2.5-flash", True)

        self.assertGreater(savings_gpt["percent_savings"], 97.0)
        self.assertGreater(savings_claude["percent_savings"], 97.5)
        self.assertGreater(savings_gpt["net_savings_usd"], 7_000.0)
        self.assertGreater(savings_claude["net_savings_usd"], 10_000.0)

    def test_enterprise_benchmarks_exports(self):
        """Verify JSON and Markdown report export generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "benchmarks.json")
            md_path = os.path.join(tmpdir, "benchmarks.md")

            self.benchmarker.export_summary_json(json_path)
            self.benchmarker.export_summary_markdown(md_path)

            self.assertTrue(os.path.exists(json_path))
            self.assertTrue(os.path.exists(md_path))

            with open(json_path) as f:
                data = json.load(f)
                self.assertEqual(data["fleet_size"], 4)
                self.assertIn("gemini-2.5-flash", data["projections"]["models"])

            with open(md_path) as f:
                md = f.read()
                self.assertIn("Google Cloud Vertex AI", md)
                self.assertIn("Prompt Caching Advantage", md)

    # ── 4. FLEET GOVERNANCE MATRIX AUDIT TESTS ────────────────────────────────

    def test_fleet_governance_matrix_audit(self):
        """Verify FleetGovernanceAuditor audits all 4 archetypes at Grade A+."""
        stats = self.governance.audit_fleet()
        self.assertEqual(stats["total_archetypes"], 4)
        self.assertEqual(stats["fleet_grade"], "A+")
        self.assertEqual(stats["fleet_readiness_pct"], 100.0)
        self.assertEqual(stats["zero_leak_security_compliance"], "100.0%")
        self.assertEqual(stats["offline_determinism"], "100.0%")
        self.assertLess(stats["average_p95_sla_ms"], 120.0)

        table = self.governance.format_ascii_table()
        self.assertIn("Williams' Agent Framework", table)
        self.assertIn("Stock & News Monitor", table)
        self.assertIn("Travel Agency Negotiation", table)

    def test_fleet_governance_exports(self):
        """Verify fleet governance JSON and Markdown export generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "governance.json")
            md_path = os.path.join(tmpdir, "governance.md")

            self.governance.export_summary_json(json_path)
            self.governance.export_summary_markdown(md_path)

            self.assertTrue(os.path.exists(json_path))
            self.assertTrue(os.path.exists(md_path))

            with open(json_path) as f:
                data = json.load(f)
                self.assertEqual(data["audit_summary"]["total_archetypes"], 4)

            with open(md_path) as f:
                md = f.read()
                self.assertIn("4-Archetype Enterprise Governance Matrix", md)
                self.assertIn("Grade A+", md)


if __name__ == "__main__":
    unittest.main()
