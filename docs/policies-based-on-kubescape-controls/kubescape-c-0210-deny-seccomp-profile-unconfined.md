# Kubescape C-0210: Deny seccomp profile Unconfined

## Why this policy is required:
Running containers with an unconfined seccomp profile exposes the host kernel to a large attack surface. Seccomp profiles restrict the system calls a container can make, and setting `seccompProfile.type` to `Unconfined` disables this protection entirely. This policy enforces that every container defines a seccomp profile other than Unconfined.

## Severity Level: High

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
This Policy checks every container and initContainer for a seccomp profile. It first checks if the container has `securityContext.seccompProfile.type` set; if so, that value must not be `Unconfined`. If the container does not set its own seccomp profile, the pod-level `securityContext.seccompProfile.type` is checked instead. If no seccomp profile is defined at any level, or if the effective profile is `Unconfined`, the resource is denied.

Windows pods (`spec.os.name: windows`) are skipped. The API server does not allow `seccompProfile` on them at all, so they could never pass, and Pod Security Admission skips the same check for them.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
