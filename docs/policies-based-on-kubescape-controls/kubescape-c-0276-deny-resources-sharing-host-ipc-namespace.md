# Kubescape C-0276: Minimize the admission of containers wishing to share the host IPC namespace

## Why this policy is required:
A container running in the host's IPC namespace can use IPC to interact with processes outside the container. There should be at least one admission control policy defined which does not permit containers to share the host IPC namespace.

If you need to run containers which require `hostIPC`, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks the pod spec of the resource:
* If `hostIPC` is `not set` or `set to false`, the resource is allowed. If it is `set to true`, the resource is denied from being deployed in the cluster.

The `hostPID` field is covered separately by C-0275. C-0038 checks both fields together.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
