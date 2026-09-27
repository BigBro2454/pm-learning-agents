#!/usr/bin/env python3
"""Unified CLI Runner for Applied AI Agent Architecture Lab.

Orchestrates execution, interactive demos, and validation across 4 production agent archetypes:
  1. Stock & News Monitor (Perception -> Reasoning -> Action -> Memory Loop)
  2. Deep-Dive Researcher (Goal Decomposition & Plan-Execute-Verify Loop)
  3. Customer Support Router (Autonomy Spectrum, RAG & Confidence Escalation)
  4. Travel Agency (Multi-Agent Adversarial Debate & Constraint Negotiation)
"""

import argparse
import os
import subprocess
import sys
import unittest

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_CATALOG = {
    "1": {
        "id": "1",
        "alias": "stock-monitor",
        "name": "Market & News Intelligence Agent",
        "archetype": "Autonomous Monitoring Loop",
        "properties": "High Reactivity | Moderate Autonomy | Low Social Ability",
        "path": os.path.join(BASE_DIR, "project-1-stock-monitor"),
        "script": "src/main.py",
    },
    "2": {
        "id": "2",
        "alias": "deep-researcher",
        "name": "Deep Information Retrieval & Synthesis Agent",
        "archetype": "Goal Decomposition & Plan-Execute",
        "properties": "High Proactivity | Moderate Reactivity | Low Social Ability",
        "path": os.path.join(BASE_DIR, "project-2-deep-researcher"),
        "script": "src/main.py",
    },
    "3": {
        "id": "3",
        "alias": "support-router",
        "name": "Customer Support Triage & Safety Router",
        "archetype": "Autonomy Spectrum & Policy Escalation",
        "properties": "Variable Autonomy | High Reactivity | Human-in-the-Loop",
        "path": os.path.join(BASE_DIR, "project-3-support-router"),
        "script": "src/main.py",
    },
    "4": {
        "id": "4",
        "alias": "travel-agency",
        "name": "Multi-Agent Constraint Negotiation System",
        "archetype": "Collaborative Multi-Agent Debate",
        "properties": "High Social Ability | High Proactivity | Bounded Autonomy",
        "path": os.path.join(BASE_DIR, "project-4-travel-agency"),
        "script": "src/main.py",
    },
}


def print_catalog():
    print("=" * 80)
    print("🤖 Applied AI Agent Architecture Lab - Project Catalog")
    print("=" * 80)
    print(f"{'#':<3} | {'Alias':<16} | {'Archetype':<32} | {'Properties'}")
    print("-" * 80)
    for p in PROJECT_CATALOG.values():
        print(f"{p['id']:<3} | {p['alias']:<16} | {p['archetype']:<32} | {p['properties']}")
    print("=" * 80 + "\n")


def run_tests():
    print("🧪 Running Applied AI Agent Test Suite...\n")
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.join(BASE_DIR, "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


def run_project(project_key: str, extra_args=None):
    # Resolve alias or ID
    matched = None
    for p in PROJECT_CATALOG.values():
        if project_key in (p["id"], p["alias"]):
            matched = p
            break

    if not matched:
        print(f"❌ Unknown project '{project_key}'. Choose from 1, 2, 3, 4 or run with --list.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GEMINI_API_KEY is not set.")
        print("   Set it in your terminal: export GEMINI_API_KEY='your-key-here'")
        print("   Or create a .env file (see .env.example)\n")

    print(f"🚀 Launching Project {matched['id']}: {matched['name']} [{matched['archetype']}]...")
    print(f"📁 Working Directory: {matched['path']}\n")

    cmd = [sys.executable, matched["script"]]
    if extra_args:
        cmd.extend(extra_args)

    env = os.environ.copy()
    env["PYTHONPATH"] = matched["path"] + (":" + env.get("PYTHONPATH", "") if env.get("PYTHONPATH") else "")

    try:
        subprocess.run(cmd, cwd=matched["path"], env=env, check=True)
    except KeyboardInterrupt:
        print("\n👋 Execution terminated by user.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Project execution exited with code {e.returncode}")


def run_benchmarks(mock: bool = True, iterations: int = 3, export_dir: str = None):
    """Execute cross-archetype performance, token, and cost benchmark suite."""
    from benchmarks.archetype_benchmarker import ArchetypeBenchmarker
    mode = "mock" if mock else "live"
    print(f"\n⚡ Initializing Cross-Archetype Benchmark Harness (Mode: {mode.upper()})...")
    benchmarker = ArchetypeBenchmarker(mode=mode)
    report = benchmarker.run_all(iterations=iterations)
    benchmarker.print_cli_summary(report)

    if export_dir:
        os.makedirs(export_dir, exist_ok=True)
        json_path = os.path.join(export_dir, "benchmark_summary.json")
        md_path = os.path.join(export_dir, "benchmark_summary.md")
        benchmarker.export_json(report, json_path)
        benchmarker.export_markdown(report, md_path)
        print(f"📁 Benchmark reports successfully exported to:")
        print(f"   JSON:     {json_path}")
        print(f"   Markdown: {md_path}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Applied AI Agent Architecture Lab CLI - Google Gemini & Williams' Framework"
    )
    parser.add_argument(
        "--project", "-p",
        choices=["1", "2", "3", "4", "stock-monitor", "deep-researcher", "support-router", "travel-agency"],
        help="Project to execute (1-4 or name)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all agent archetypes and property mappings"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run unit test suite validating schemas and message buffers"
    )
    parser.add_argument(
        "--benchmark", "-b",
        action="store_true",
        help="Execute cross-archetype token, cost, and latency comparative benchmark suite"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        default=True,
        help="Run benchmark in deterministic offline mock mode (default: True)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Run benchmark against live Google Gemini 2.5 Flash API"
    )
    parser.add_argument(
        "--iterations", "-i",
        type=int,
        default=3,
        help="Number of iterations per archetype (default: 3)"
    )
    parser.add_argument(
        "--export-dir",
        type=str,
        default=None,
        help="Directory path to export benchmark JSON and Markdown scorecards"
    )

    args, unknown = parser.parse_known_args()

    if args.list:
        print_catalog()
        return

    if args.test:
        run_tests()
        return

    if args.benchmark:
        is_mock = not args.live
        run_benchmarks(mock=is_mock, iterations=args.iterations, export_dir=args.export_dir)
        return

    if args.project:
        run_project(args.project, unknown)
    else:
        print_catalog()
        print("Usage:")
        print("  python run_lab.py --project 1              # Run Stock Monitor")
        print("  python run_lab.py --project 2              # Run Deep Researcher")
        print("  python run_lab.py --project 3              # Run Support Router")
        print("  python run_lab.py --project 4              # Run Travel Agency")
        print("  python run_lab.py --benchmark              # Run cross-archetype benchmark")
        print("  python run_lab.py --test                   # Run automated tests\n")


if __name__ == "__main__":
    main()

