# Kubescape C-0009: Deny resources with memory or CPU limits not set

## Why this policy is required:
CPU and memory resources should have a limit set for every container or a namespace to prevent resource exhaustion.

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
### This Policy checks for every container and init container in the resource, including native sidecars (init containers with `restartPolicy: Always`):
* If `resources.limits.memory` is set.
* If `resources.limits.cpu` is set.


If any of the above two checks fail, the resource is denied from being deployed in the cluster.

Ephemeral containers (added with `kubectl debug`) are not checked, because the Kubernetes API does not allow `resources` on ephemeral containers.


## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)