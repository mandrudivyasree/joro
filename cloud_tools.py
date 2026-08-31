def get_service_health(service_name: str) -> dict:
    """Returns the current health information for a cloud service."""

    return {
        "service": service_name,
        "status": "UNHEALTHY",
        "error_rate": "37%",
        "recent_errors": [
            "HTTP 503",
            "Connection timeout",
            "Container startup failure"
        ]
    }
def get_recent_logs(service_name: str) -> dict:
    """Returns recent log information for a cloud service."""

    return {
        "service": service_name,
        "logs": [
            "Container failed to start: missing environment variable DATABASE_URL",
            "Health check failed after 3 attempts",
            "HTTP 503 returned to client",
            "Container restarted automatically"
        ]
    }
def get_simulated_metric_status(service_name: str) -> dict:
    """Returns recent performance metrics for a cloud service."""

    return {
        "service": service_name,
        "cpu_utilization": "92%",
        "request_latency": "4.8 seconds",
        "error_rate": "37%",
        "requests_per_second": 145
    }
from google.cloud import monitoring_v3
from google.protobuf.duration_pb2 import Duration
from google.protobuf.timestamp_pb2 import Timestamp

def get_cpu_utilization() -> dict:
    """Reads recent CPU utilization data from Google Cloud Monitoring."""

    client = monitoring_v3.MetricServiceClient()
    project_name = "projects/project_id"

    interval = monitoring_v3.TimeInterval()

    end_time = Timestamp()
    end_time.GetCurrentTime()

    start_time = Timestamp()
    start_time.FromSeconds(end_time.ToSeconds() - 600)

    interval.start_time = start_time
    interval.end_time = end_time

    aggregation = monitoring_v3.Aggregation(
        alignment_period=Duration(seconds=300),
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": 'metric.type="compute.googleapis.com/instance/cpu/utilization"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    values = []

    for series in results:
        for point in series.points:
            values.append(point.value.double_value)

    if not values:
        return {
            "status": "NO_DATA",
            "message": "No CPU utilization data was found in the last 10 minutes.",
        }

    average_cpu = sum(values) / len(values)

    return {
        "status": "OK",
        "metric": "CPU utilization",
        "average": round(average_cpu * 100, 2),
        "unit": "%",
        "samples": len(values),
    }


def restart_service(service_name: str) -> dict:
    """Simulates restarting a cloud service after an incident."""

    return {
        "service": service_name,
        "action": "restart",
        "status": "SIMULATED",
        "message": f"Restart request for {service_name} was simulated successfully.",
    }

def verify_service_recovery(service_name: str) -> dict:
    """Verifies whether a service recovered after a corrective action."""

    health = get_service_health(service_name)

    if health.get("status") == "HEALTHY":
        return {
            "service": service_name,
            "status": "RECOVERED",
            "message": f"{service_name} recovered successfully after the corrective action.",
        }

    return {
        "service": service_name,
        "status": "STILL_UNHEALTHY",
        "error_rate": health.get("error_rate"),
        "recent_errors": health.get("recent_errors"),
        "message": f"{service_name} is still unhealthy. Further investigation is required.",
    }

def check_for_incidents() -> dict:
    """Checks real Google Cloud CPU utilization for potential incidents."""

    cpu_result = get_cpu_utilization()

    if cpu_result.get("status") != "OK":
        return {
            "incident": False,
            "status": "NO_DATA",
            "message": "Unable to determine incident status because CPU data is unavailable.",
        }

    cpu = cpu_result["average"]

    if cpu >= 80:
        return {
            "incident": True,
            "severity": "HIGH",
            "reason": f"CPU utilization is {cpu}%, which exceeds the 80% threshold.",
        }

    if cpu >= 60:
        return {
            "incident": True,
            "severity": "MEDIUM",
            "reason": f"CPU utilization is {cpu}%, which exceeds the 60% threshold.",
        }

    return {
        "incident": False,
        "severity": "NORMAL",
        "reason": f"CPU utilization is {cpu}%, which is within the normal range.",
    }
