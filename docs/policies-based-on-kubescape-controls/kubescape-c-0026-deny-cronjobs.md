# Kubescape C-0026: Deny CronJobs

## Why this policy is required:
Attackers may use Kubernetes CronJob for scheduling execution of malicious code that would run as a pod in the cluster. This control lists all the CronJobs that exist in the cluster for the user to approve.

## Severity Level: Low

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob

## What does this policy do:
This policy flags every `CronJob` admitted to the cluster so it can be surfaced to the user for review. It is an audit-style control, not an enforcement: the Rego source in `kubescape/regolibrary` (`rule-deny-cronjobs`) emits an alert on every CronJob, with a base score of 1.0.

## Binding requirement: audit-only

This control is only safe when bound with `validationActions: [Audit]` or `[Warn]`. Under those actions the CronJob is admitted and a Kubernetes audit annotation or API-server warning is recorded so an operator can review it.

The default `ValidatingAdmissionPolicyBinding` shipped in this repo (`test-resources/policy-binding.yaml`) uses `validationActions: [Deny]`. Binding C-0026 with `[Deny]` will reject the admission of every CronJob in the cluster, which does not match the audit intent of the source rule. An example `[Warn]` binding is provided in `test-resources/policy-binding-warn.yaml` and is the binding the C-0026 test runs against.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
