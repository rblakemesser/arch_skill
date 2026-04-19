# Security Policy

## Supported Versions

Security fixes are handled on the current `main` branch.

## Reporting a Vulnerability

Do not report vulnerabilities in public issues.

Use GitHub private vulnerability reporting when it is available for this repository. If private reporting is unavailable, contact the repository owner directly through GitHub with a short summary and a safe way to share details.

Please include:

- affected files, commands, or install paths
- a minimal reproduction when possible
- expected impact
- whether the issue exposes credentials, local files, or remote command execution

## Scope

Security-sensitive areas include:

- install scripts and `Makefile` targets
- Stop-hook controller code
- commands that run child agents or shell commands
- remote install and SSH workflows
- documentation that instructs users to paste secrets or tokens

Do not include live credentials, private keys, or tokens in reports, issues, pull requests, or examples.
