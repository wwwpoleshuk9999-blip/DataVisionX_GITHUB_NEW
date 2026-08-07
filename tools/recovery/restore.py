import os
import json

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

HISTORY_FILE = os.path.join(
    BASE,
    "runtime",
    "recovery",
    "history.json"
)


if not os.path.exists(HISTORY_FILE):
    print("Recovery history not found")
    exit(1)


with open(HISTORY_FILE, "r") as f:
    history = json.load(f)


if not history:
    print("No checkpoints available")
    exit(0)


print("=== DataVisionX Recovery Points ===")

for i, item in enumerate(history, 1):
    print()
    print(f"[{i}]")
    print("File:", item["file"])
    print("Created:", item["created"])
    print("Branch:", item["branch"])
    print("Commit:", item["commit"])
    print("Status:", item["status"])


print()
print("Latest checkpoint:")
latest = history[-1]

print(latest["file"])
print(latest["commit"])
