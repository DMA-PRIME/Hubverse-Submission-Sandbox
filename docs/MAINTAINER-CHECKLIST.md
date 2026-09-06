# Classroom maintainer checklist

## One-time repository settings

- [ ] Confirm `DMA-PRIME/Hubverse-Submission-Sandbox` is public.
- [ ] Protect `main` from direct student pushes.
- [ ] Require pull requests for changes to `main`.
- [ ] Keep the workflow token read-only and do not expose repository or organization secrets.
- [ ] Review the organization's GitHub Actions policy for pull requests from public forks.
- [ ] Decide who is responsible for approving first-time contributor workflow runs.
- [ ] Add the desired license, code of conduct, and moderation policy.
- [ ] Test the website, Desktop, and terminal routes from a non-administrator account.

## For each student pull request

- [ ] Confirm the head repository is the student's personal fork.
- [ ] Confirm the public practice ID is non-identifying.
- [ ] Confirm exactly one synthetic metadata file and one synthetic output file changed.
- [ ] Reject any workflow, script, configuration, instruction, binary, secret, or unrelated change.
- [ ] If GitHub shows **Awaiting approval**, inspect Files changed before approving the workflow run.
- [ ] Wait for `Validate synthetic practice submission` to pass.
- [ ] Ask the student to correct failures on the same branch and pull request.
- [ ] Add a brief instructor acknowledgment after the check passes.
- [ ] Close the pull request **without merging**.

## Why practice pull requests are not merged

Each student's fork and branch is an independent workspace. Closing successful practice pull requests without merging allows many simultaneous submissions while keeping `main` clean and avoiding filename conflicts or accumulated classroom data.

Closed pull requests remain public. Never treat closure or branch deletion as a way to remove sensitive information; sensitive information must never be uploaded.

## Periodic review

- [ ] Review open and awaiting-approval pull requests.
- [ ] Confirm the validation workflow still uses `pull_request`, a read-only token, no secrets, and GitHub-hosted runners.
- [ ] Confirm the guide and screenshot instructions use the current repository owner and name.
- [ ] Re-test the workflow after changing the validator or repository settings.
