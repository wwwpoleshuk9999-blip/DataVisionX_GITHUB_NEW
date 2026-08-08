import json
import subprocess
from pathlib import Path
from datetime import datetime, UTC


class TechnicalProfiler:
    def __init__(self, project_root="."):
        self.root = Path(project_root).resolve()

    def profile(self):
        python_files = list(self.root.rglob("*.py"))
        test_files = [
            path for path in python_files
            if "test" in path.name.lower()
        ]

        git = self._git_info()

        total_lines = 0
        for path in python_files:
            try:
                total_lines += len(
                    path.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).splitlines()
                )
            except OSError:
                continue

        if not python_files:
            state = "UNKNOWN"
            strength = 0
        elif total_lines >= 1000:
            state = "HEAVY"
            strength = 1.0
        elif total_lines >= 300:
            state = "MODERATE"
            strength = 0.6
        else:
            state = "LIGHT"
            strength = 0.25

        return {
            "project": self.root.name,
            "timestamp": datetime.now(UTC).isoformat(),
            "profile": {
                "python_files": len(python_files),
                "test_files": len(test_files),
                "python_lines": total_lines,
                "profile_state": state,
                "profile_strength": strength,
            },
            "git": git,
            "mode": "REPORT_ONLY",
            "status": "READY",
        }

    def _git_info(self):
        def run(command):
            try:
                return subprocess.check_output(
                    command,
                    cwd=self.root,
                    stderr=subprocess.DEVNULL,
                    text=True
                ).strip()
            except (
                subprocess.CalledProcessError,
                FileNotFoundError
            ):
                return None

        return {
            "branch": run(
                ["git", "branch", "--show-current"]
            ),
            "commit": run(
                ["git", "rev-parse", "HEAD"]
            ),
            "status": (
                "CLEAN"
                if run(
                    ["git", "status", "--porcelain"]
                ) == ""
                else "DIRTY"
            ),
        }


def save_report(data, output="runtime/recovery/devtools_profiler_report.json"):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )
    return path


if __name__ == "__main__":
    profiler = TechnicalProfiler()
    report = profiler.profile()
    path = save_report(report)

    print(json.dumps(
        report,
        indent=4,
        ensure_ascii=False
    ))
    print(f"Report: {path}")
