kubescape-c-0048-deny-workloads-with-hostpath-mounts
# Kubescape C-0048: Deny resources with hostPath mounts

## Why this policy is required:
Mounting host directory to the container can be used by attackers to get access to the underlying host.

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
This Policy checks if `hostPath` is mounted to the resource. If `hostPath` is mounted, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)