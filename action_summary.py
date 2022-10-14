import os

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
        os.environ["GITHUB_STEP_SUMMARY"] = fr.read()
        
    print("Job summary report created {}".format(os.path.abspath("job_summary.md")))
     
