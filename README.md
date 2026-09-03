# DMAPRIME Hubverse Submission Sandbox

This is a Hubverse-shaped teaching repository for practicing the mechanics of a model submission: choose the correct path, create a branch, commit only the intended files, open a pull request, read automated checks, and correct the same branch.

It is deliberately a sandbox, not a live forecasting challenge. A successful practice pull request is not a submission to CDC, ECDC, a Scenario Modeling Hub, or any other operational hub.

## The shortest path

1. Open `practice-files/` and download one forecast or scenario example plus `student-demo.yml`.
2. Replace `student-demo` in the metadata filename and contents with your own `<team>-<model>` identifier.
3. Rename the output as `<round_id>-<team>-<model>.<extension>`.
4. Put the metadata at `model-metadata/<team>-<model>.yml`.
5. Put the output at `model-output/<team>-<model>/<round_id>-<team>-<model>.<extension>`.
6. Create a branch, commit the two files, and open a pull request.
7. Read the practice validation result. If it fails, update the same branch.

For the included example, the paths are:

```text
model-metadata/student-demo.yml
model-output/student-demo/2026-09-05-student-demo.csv
```

## What the checks teach

The included validator checks the relationships that most often confuse first-time submitters:

- `model_id` is `<team_abbr>-<model_abbr>`.
- the metadata filename equals `<model_id>.yml` or `<model_id>.yaml`;
- the output subfolder equals `<model_id>`;
- the output filename ends in `-<model_id>`;
- the round identifier appears before the model ID;
- CSV and TSV files have either the practice forecast or practice scenario columns;
- when the round identifier is an ISO date, it agrees with `reference_date` or `origin_date` in the tabular file;
- a metadata file exists for the model.

The checker intentionally does not claim to reproduce every operational hub rule. Real hubs can require different columns, formats, targets, dates, permissions, and deadlines.

## Practice tracks

The repository accepts two teaching schemas:

- Forecast: `reference_date,target,horizon,target_end_date,location,output_type,output_type_id,value`
- Scenario: `origin_date,scenario_id,target,horizon,location,age_group,output_type,output_type_id,value,run_grouping,stochastic_run`

The practice repository accepts CSV or TSV so students can inspect the examples. It also checks the path and Parquet magic bytes for `.parquet` and `.gz.parquet` files, but it does not perform full Parquet schema validation.

## Local validation

Python 3 is the only requirement:

```bash
python scripts/validate_submission.py
```

You can also validate one or more paths:

```bash
python scripts/validate_submission.py \
  model-metadata/student-demo.yml \
  model-output/student-demo/2026-09-05-student-demo.csv
```

## Safety and publication status

This package is only a local repository blueprint. It has no Git history, no remote, no credentials, and no code that can create or modify a GitHub repository. Publishing it later must be a separate, deliberate action by the repository owner.

The companion standalone HTML guide likewise performs no authentication, GitHub API call, upload, commit, push, or pull-request action. It reads user-selected files locally in the browser.

## Before publishing

- Choose the final repository organization and name.
- Decide whether pull requests should be public and whether branches should be deleted after practice.
- Add the desired license, code of conduct, and moderation policy.
- Review and approve the GitHub Actions workflow.
- Decide whether students may use real forecast files or only synthetic practice data.
- Test with a non-administrator student account.

Created for the Hubverse Support Toolkit by DMAPRIME at Clemson University.
