#!/usr/bin/env python3
"""Unit and integration tests for ArchetypeBenchmarker."""

import os
import shutil
import tempfile
import unittest

from benchmarks.archetype_benchmarker import (
    ArchetypeBenchmarker,
    ArchetypeMetrics,
    BenchmarkReport,
    PRICE_PER_1M_PROMPT,
    PRICE_PER_1M_COMPLETION,
)


class TestArchetypeBenchmarker(unittest.TestCase):
    """Test suite validating cross-archetype performance and cost benchmarking."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.benchmarker = ArchetypeBenchmarker(mode="mock")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_single_archetype_metrics_structure(self):
        """Verify Archetype 1 produces valid latency, token counts, and cost metrics."""
        m1 = self.benchmarker.benchmark_archetype_1(iterations=2)
        self.assertIsInstance(m1, ArchetypeMetrics)
        self.assertEqual(m1.archetype_id, "1")
        self.assertGreater(m1.mean_latency_ms, 0)
        self.assertGreater(m1.total_tokens, 0)
        self.assertEqual(m1.prompt_tokens + m1.completion_tokens, m1.total_tokens)
        self.assertGreater(m1.cost_per_1k_runs_usd, 0)
        self.assertEqual(m1.contract_conformance_rate, 100.0)

    def test_pricing_and_cost_calculation(self):
        """Verify token economics adhere strictly to Gemini 2.5 Flash enterprise pricing formulas."""
        prompt_tokens = 1000
        completion_tokens = 500
        expected_cost_run = (prompt_tokens / 1e6 * PRICE_PER_1M_PROMPT) + (
            completion_tokens / 1e6 * PRICE_PER_1M_COMPLETION
        )
        self.assertAlmostEqual(expected_cost_run, 0.000225, places=6)

    def test_full_suite_run_and_aggregation(self):
        """Verify all 4 archetypes execute and generate correct summary statistics."""
        report = self.benchmarker.run_all(iterations=2)
        self.assertIsInstance(report, BenchmarkReport)
        self.assertEqual(report.total_archetypes, 4)
        self.assertEqual(len(report.archetypes), 4)

        # Check that archetypes 1-4 are all present
        ids = [a.archetype_id for a in report.archetypes]
        self.assertEqual(ids, ["1", "2", "3", "4"])

        # Check fleet summary metrics
        self.assertIn("average_latency_ms", report.fleet_summary)
        self.assertIn("aggregate_cost_per_1k_suite_runs_usd", report.fleet_summary)
        self.assertGreater(report.fleet_summary["average_latency_ms"], 0)
        self.assertGreater(report.fleet_summary["total_benchmark_tokens"], 0)

    def test_export_json_and_markdown(self):
        """Verify structured JSON and Google L5 Markdown reports export cleanly."""
        report = self.benchmarker.run_all(iterations=2)
        json_file = os.path.join(self.temp_dir, "benchmark_summary.json")
        md_file = os.path.join(self.temp_dir, "benchmark_summary.md")

        self.benchmarker.export_json(report, json_file)
        self.benchmarker.export_markdown(report, md_file)

        self.assertTrue(os.path.exists(json_file))
        self.assertTrue(os.path.exists(md_file))

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Applied AI Agent Archetypes: Cross-Archetype Benchmark Report", content)
            self.assertIn("Stock & News Monitor", content)
            self.assertIn("Travel Agency Debate", content)


if __name__ == "__main__":
    unittest.main()
