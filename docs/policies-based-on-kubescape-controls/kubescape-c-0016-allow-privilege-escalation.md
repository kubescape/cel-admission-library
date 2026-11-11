# Kubescape C-0016: Deny if allowPrivilegeEscalation is not set

## Why this policy is required:
Attackers may gain access to a container and uplift its privilege to enable excessive capabilities.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
### This Policy checks for every container (regular, init, and ephemeral) in the resource:
* If `securityContext.allowPrivilegeEscalation` is explicitly set to `false`. If it is missing,
  set to `true`, or the entire `securityContext` is absent, the resource is denied from being
  deployed in the cluster.

Windows pods (`spec.os.name: windows`) are skipped. The API server does not allow `allowPrivilegeEscalation` on them at all, so they could never pass, and Pod Security Admission skips the same check for them.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)