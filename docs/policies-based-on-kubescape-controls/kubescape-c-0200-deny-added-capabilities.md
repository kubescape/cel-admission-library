# Kubescape C-0200: Deny added capabilities

## Why this policy is required:
Relying on container runtime defaults for capabilities is unsafe — default sets vary across runtimes and may include capabilities that aren't needed by the workload. Requiring explicit `drop: ["ALL"]` follows the PSA restricted baseline, ensuring only explicitly needed capabilities are present.

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
This Policy requires every container, initContainer, and ephemeralContainer to have `securityContext.capabilities.drop` set to `["ALL"]`. This enforces that all default capabilities are dropped, and workloads must explicitly add back only the capabilities they need. If any container does not have `drop: ["ALL"]`, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
