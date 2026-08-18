# Kubescape C-0195: Minimize the admission of containers wishing to share the host IPC namespace

## Why this policy is required:
A container running in the host's IPC namespace can use shared memory to interact with processes outside the container. There should be at least one admission control policy defined which does not permit containers to share the host IPC namespace.

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

The `hostPID` field is covered separately by C-0194.

## How this relates to C-0276 and C-0038:
C-0276 is the same check on the same field, from a different framework. The two policies deny the same resources, and they exist separately because the library keys a policy to exactly one control ID. C-0038 checks `hostPID` and `hostIPC` together, so it denies a superset of what this one does.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
