import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE))

from devtools.profiler.profiler import TechnicalProfiler


def run_scenario(name, project_root, expected_state):
    profiler = TechnicalProfiler(project_root)
    result = profiler.profile()

    passed = (
        result["profile"]["profile_state"]
        == expected_state
    )

    return {
        "scenario": name,
        "result": result,
        "expected": {
            "profile_state": expected_state
        },
        "passed": passed,
    }


def main():
    base = BASE / "runtime" / "recovery" / "profiler_scenario_tmp"
    base.mkdir(parents=True, exist_ok=True)

    empty = base / "empty"
    empty.mkdir(exist_ok=True)

    light = base / "light"
    light.mkdir(exist_ok=True)
    (light / "one.py").write_text(
        "print('hello')\n",
        encoding="utf-8"
    )

    moderate = base / "moderate"
    moderate.mkdir(exist_ok=True)
    (moderate / "many.py").write_text(
        "\n".join(["x = 1"] * 300),
        encoding="utf-8"
    )

    heavy = base / "heavy"
    heavy.mkdir(exist_ok=True)
    (heavy / "many.py").write_text(
        "\n".join(["x = 1"] * 1000),
        encoding="utf-8"
    )

    tests = [
        run_scenario(
            "empty_project",
            empty,
            "UNKNOWN"
        ),
        run_scenario(
            "light_project",
            light,
            "LIGHT"
        ),
        run_scenario(
            "moderate_project",
            moderate,
            "MODERATE"
        ),
        run_scenario(
            "heavy_project",
            heavy,
            "HEAVY"
        ),
    ]

    status = (
        "READY"
        if all(item["passed"] for item in tests)
        else "FAILED"
    )

    report = {
        "project": BASE.name,
        "engine": "DTA-006.2",
        "mode": "SCENARIO_TEST",
        "tests": tests,
        "status": status,
    }

    report_path = (
        BASE
        / "runtime"
        / "recovery"
        / "devtools_profiler_scenarios_report.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print(json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    ))
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
