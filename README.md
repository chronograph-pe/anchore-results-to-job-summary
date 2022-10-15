# anchore-results-to-job-summary

This action posts Anchore container image scan results to a Github summary report. 

[anchore/scan-action](https://github.com/anchore/scan-action) is  a GitHub Action for invoking the Grype scanner and returning the vulnerabilities found, and optionally fail if a vulnerability is found with a configurable severity level.

## Usage

### Pre-requisites
Create a workflow `.yml` file in your repositories `.github/workflows` directory. An [example workflow](#example-workflow) is available below. For more information, reference the GitHub Help Documentation for [Creating a workflow file](https://help.github.com/en/articles/configuring-a-workflow#creating-a-workflow-file).

At this time only `JSON` Anchore results files are supported. `SARIF` in the works. 


### Inputs

* `results_file` -  The Anchore results file name and path. Default value is `results.json`
* `severity_threshold` - The severity threshold you want to include in your report. Default value is `medium`. Supported values are `low, medium, high, and critical`. Any value set, will output results for that value and higher severities. 

### Outputs

No outputs, but the results will be appended to `$GITHUB_STEP_SUMMARY` which is used to create a Github job summary report. [Learn more -> Super charing github actions with job summaries.](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/)

### Example workflow

```yaml
name: Container Image CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1

      - name: build local container
        uses: docker/build-push-action@v2
        with:
          tags: localbuild/testimage:latest
          push: false
          load: true
          file: ./Dockerfile
      
      - uses: anchore/scan-action@v3
        with:
          image: "localbuild/testimage:latest"
          fail-build: false
          output-format: json

      - name: Create Job Description
        id: createjd
        uses: chronograph-pe/anchore-results-to-job-summary@main
        with:
          results_file: ${{ steps.scan.outputs.json }}
          severity_threshold: critical

```

