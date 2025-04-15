# Kubescape C-0042: Deny resources with SSH server running.

## Why this policy is required:
SSH server that is running inside a container may be used by attackers. If attackers gain valid credentials to a container, whether by brute force attempts or by other methods (such as phishing), they can use it to get remote access to the container by SSH.

## Severity Level: Low

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Service
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks
* If the `port` and `targetPort` is not an `SSH port(22/2222)` if the resource is `Service`.
* If all the Containers in the workload does not have `hostPort` or `containerPort` set to an `SSH port(22/2222)`.

If any of the above check fails, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)