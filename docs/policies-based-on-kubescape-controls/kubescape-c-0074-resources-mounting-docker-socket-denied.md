# Kubescape C-0074: Deny resources mounting Docker socket

## Why this policy is required:
Mounting Docker socket (Unix socket) enables container to access Docker internals, retrieve sensitive information and execute Docker commands, if Docker runtime is available.

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
This Policy checks if `hostPath.path` is set to `/var/run/docker.sock` or `/var/lib/docker`. If so,the resource will have access to docker internals. Therefore, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)