import json
import os
import action_summary


results_file = os.getenv("RESULTS_FILE", "results.json")
severity_threshold = os.getenv("SEVERITY_THRESHOLD", "medium")

def main():
    r = []

    if not os.path.exists(results_file):
        print("{} result_file not found".format(results_file))
        exit(1)

    with open(results_file, "r") as f:
        results = json.load(f)

    if not results.get("matches"):
        print("no results found")
        exit(0)

    valid_severities = generate_thresholdes(severity_threshold)

    for match in results.get("matches"):
        vulnerability = match.get("vulnerability")
        artifact = match.get("artifact")

        if vulnerability.get("severity").lower() in valid_severities:
            severity = vulnerability.get("severity")
            description = vulnerability.get("description")
            cve_id = vulnerability.get("id")
            name = artifact.get("name")
            installed = artifact.get("version")
            fixed_state = vulnerability.get("fix").get("state")
            fixed_versions = vulnerability.get("fix").get("versions")

            r.append({
                "severity": severity,
                "description": description,
                "cve_id": cve_id,
                "name": name,
                "installed": installed,
                "fixed_state": fixed_state,
                "fixed_versions": fixed_versions
            })

    action_summary.create(r)


def generate_thresholdes(severity_threshold):
    valid_severities = []

    if severity_threshold == "negligible":
        valid_severities = ["negligible", "low", "medium", "high", "critical"]
    elif severity_threshold == "low":
        valid_severities = ["low", "medium", "high", "critical"]
    elif severity_threshold == "medium":
        valid_severities = ["medium", "high", "critical"]
    elif severity_threshold == "high":
        valid_severities = ["high", "critical"]
    elif severity_threshold == "critical":
        valid_severities = ["critical"]  

    return valid_severities



if __name__ == "__main__":
    main()