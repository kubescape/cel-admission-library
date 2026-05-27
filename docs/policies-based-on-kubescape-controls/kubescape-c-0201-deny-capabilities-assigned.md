# Kubescape C-0201: Deny capabilities assigned

## Why this policy is required:
Assigning capabilities to containers — whether adding new ones or selectively dropping some — goes against the principle of least privilege for secure workloads. The PSA restricted standard requires that all capabilities be dropped and none be added, ensuring containers run with the absolute minimum privilege set.

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
This Policy enforces the strictest capability posture: every container must have `securityContext.capabilities.drop` set to `["ALL"]` AND must not have any capabilities in `securityContext.capabilities.add`. This is stricter than C-0200, which allows adding back specific capabilities. If any container violates either condition, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
