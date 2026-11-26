# Kubescape C-0199: Deny NET_RAW capability

## Why this policy is required:
The NET_RAW capability allows containers to open raw sockets, which can be misused for network spoofing, packet injection, and other network attacks. Blocking this capability reduces the attack surface for containerized workloads.

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
This Policy checks if any container, initContainer, or ephemeralContainer has the NET_RAW capability explicitly added in `securityContext.capabilities.add`. If NET_RAW is found, the resource is denied from being deployed in the cluster.

Windows pods (`spec.os.name: windows`) are skipped. The API server does not allow `capabilities` on them at all, so they could never pass, and Pod Security Admission skips the same check for them.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
