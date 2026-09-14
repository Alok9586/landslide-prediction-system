import time
import csv
import os
from risk_engine import run_one_cycle

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "risk_log.csv")
CYCLE_SECONDS = 15   # how often to check - use 15s for testing, 15 min (900) for real deployment

def log_result(result):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()   # only write column headers once
        writer.writerow(result)

def main():
    print(f"Starting risk monitoring loop (every {CYCLE_SECONDS}s). Press Ctrl+C to stop.\n")
    while True:
        result = run_one_cycle(risk_bias="normal")   # swap to "danger" to test alerts
        log_result(result)

        print(f"[{result['timestamp']}] Risk: {result['risk_level']} "
              f"(probability={result['risk_probability']})")

        if result["risk_level"] in ("HIGH", "CRITICAL"):
            print(f"  🚨 ALERT: {result['risk_level']} risk detected! (alert wiring comes in Step 8)")

        time.sleep(CYCLE_SECONDS)

if __name__ == "__main__":
    main()