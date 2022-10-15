import json
import os
import re


results_file = os.getenv("results_file", "results.json")
severity_threshold = os.getenv("severity_threshold", "critical")

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

    create(r)


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


def create(results):
        
    with open ("job_summary.md", "w") as f:
        f.write("# Container Scan Job Summary \n")
        f.write(" --- \n")
        f.write("### Vulnerabilities\n")
        f.write("")
        f.write("")
        if not results:
            f.write("#### No vulnerabilities found\n\n")
        else:
            f.write("| Severity | CVE ID | Name | Installed Version | Fixed State | Fixed Version | Description\n")
            f.write("| ------ | ------ | ------ | ------ | ------ | ------ | ------ | \n")
            for result in results:
                f.write("| {} | {} | {} | {} | {} | {} | {} |\n".format(
                    result["severity"], result["cve_id"], result["name"], result["installed"],
                    result["fixed_state"], result["fixed_versions"], result["description"]
                ))

    with open("job_summary.md", "r")  as fr:
        summary =  fr.read()

    with open(os.getenv('GITHUB_STEP_SUMMARY'), "a") as fr:
        fr.write(summary)

    print("Job summary report created {}".format(os.path.abspath("job_summary.md")))


if __name__ == "__main__":
    main()