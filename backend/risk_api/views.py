import csv
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

def get_log_path():
    # engine/risk_log.csv lives one level up from backend/, in the project root
    project_root = os.path.dirname(settings.BASE_DIR)
    return os.path.join(project_root, "engine", "risk_log.csv")

@api_view(["GET"])
def risk_readings(request):
    log_path = get_log_path()

    if not os.path.exists(log_path):
        return Response({"error": "No readings logged yet."}, status=404)

    readings = []
    with open(log_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            readings.append(row)

    # Return most recent readings first, limit to last 100 for a clean dashboard
    readings = readings[-100:]
    readings.reverse()

    return Response({"count": len(readings), "readings": readings})

@api_view(["GET"])
def latest_risk(request):
    log_path = get_log_path()

    if not os.path.exists(log_path):
        return Response({"error": "No readings logged yet."}, status=404)

    with open(log_path, newline="") as f:
        reader = list(csv.DictReader(f))

    if not reader:
        return Response({"error": "Log file is empty."}, status=404)

    return Response(reader[-1])   # just the most recent reading