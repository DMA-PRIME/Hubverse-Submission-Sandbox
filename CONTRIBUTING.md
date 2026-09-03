# Practice submission instructions

This repository is for learning. Do not submit sensitive, proprietary, embargoed, or operational forecast data.

## 1. Pick a model ID

Create a model ID as `<team_abbr>-<model_abbr>`.

- Use letters, numbers, and underscores inside each part.
- Use exactly one hyphen between the team and model abbreviations.
- Example: `student-demo`.

## 2. Prepare metadata

Copy `practice-files/student-demo.yml` and rename it `<model_id>.yml`.

The filename and the values of `team_abbr`, `model_abbr`, and `model_id` must all agree.

## 3. Prepare output

Choose either practice schema in `practice-files/`. Keep the exact column names.

Name the file:

```text
<round_id>-<model_id>.<extension>
```

An ISO date is the clearest practice round ID. Example:

```text
2026-09-05-student-demo.csv
```

## 4. Put both files in the exact paths

```text
model-metadata/<model_id>.yml
model-output/<model_id>/<round_id>-<model_id>.<extension>
```

## 5. Propose the change

Use a new branch. Commit only your metadata and output. Open a pull request to `main`, wait for the practice checks, and correct failures on the same branch.

Do not treat a green sandbox check as proof that a file will pass a real hub's validations. Always use that hub's current instructions and task configuration.
