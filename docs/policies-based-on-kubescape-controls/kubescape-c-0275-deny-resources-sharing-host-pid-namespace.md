# Kubescape C-0275: Minimize the admission of containers wishing to share the host process ID namespace

## Why this policy is required:
A container running in the host's PID namespace can inspect processes running outside the container. If the container also has access to ptrace capabilities this can be used to escalate privileges outside of the container. There should be at least one admission control policy defined which does not permit containers to share the host PID namespace.

If you need to run containers which require `hostPID`, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
* If `hostPID` is `not set` or `set to false`, the resource is allowed. If it is `set to true`, the resource is denied from being deployed in the cluster.

The `hostIPC` field is covered separately by C-0276. C-0038 checks both fields together.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
