# Practice submission instructions

This is a public classroom repository. Use only synthetic files created for this exercise. Do not upload your real forecast, real model metadata, personal information, credentials, or restricted data.

## 1. Start from your personal fork

Fork `DMA-PRIME/Hubverse-Submission-Sandbox` into your own GitHub account. Verify that the page shows:

```text
YOUR-USERNAME/Hubverse-Submission-Sandbox
forked from DMA-PRIME/Hubverse-Submission-Sandbox
```

Do not create a new empty repository, work in another student's fork, or commit to the original repository's `main` branch.

## 2. Use your generated public practice ID

The companion guide creates an anonymous ID such as `learner-a7k9m2`.

- It must follow `<team_abbr>-<model_abbr>`.
- Use letters, numbers, and underscores inside each part.
- Use exactly one hyphen between the two parts.
- Do not use your name, student number, email address, or real model ID.

Different students can use different aliases. Even if two aliases were accidentally identical, separate forks keep their pull requests independent; instructors do not merge practice pull requests.

## 3. Download the two synthetic files

Download both files from the companion guide:

```text
<practice_model_id>.yml
<practice_date>-<practice_model_id>.csv
```

The generated YAML and CSV contain synthetic teaching values. Do not substitute the real files used to create your private hub-submission map.

## 4. Create a new branch

Create the branch shown by the guide, for example:

```text
practice-2026-09-03-learner-a7k9m2
```

Use one branch for one practice attempt. If a check fails, correct the same branch instead of opening another pull request.

## 5. Put both files at the exact paths

```text
model-metadata/<practice_model_id>.yml
model-output/<practice_model_id>/<practice_date>-<practice_model_id>.csv
```

Do not change `.github/`, `scripts/`, `hub-config/`, the README files, or another learner's files.

## 6. Review before committing

Your branch should contain exactly two new files: the generated metadata and generated output. Stop if you see real data, unrelated files, temporary files, credentials, or secrets.

## 7. Open one pull request

Open the pull request toward:

```text
base repository: DMA-PRIME/Hubverse-Submission-Sandbox
base branch: main
```

The compare repository should be your fork and the compare branch should be your practice branch.

GitHub may show **Awaiting approval** for a first-time contributor. That is normal; an instructor must inspect the proposed files before approving the workflow run.

## 8. Read checks and correct the same branch

- Yellow/pending: wait or wait for instructor workflow approval.
- Red/failed: open the check, read the first specific error, correct your files, and update the same branch.
- Green/passed: leave the pull request open for instructor acknowledgment.

## 9. Finish without merging

After acknowledging the completed practice, the instructor closes the pull request without merging it. This prevents student practice files from accumulating on `main` and lets many students practice simultaneously.

A green sandbox check is not proof that a real file will pass an operational hub. Use the real-hub map from the companion guide and re-check that hub's current instructions.
