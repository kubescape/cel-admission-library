# Kubescape C-0193: Minimize the admission of privileged containers

## Why this policy is required:
A privileged container gets almost all of the capabilities of the host, and it also loses the limits a container runtime normally applies to devices. That makes a container escape much easier, so there should be at least one admission control policy defined which does not permit privileged containers.

If you need to run privileged containers, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks every container in the resource, including init containers and ephemeral containers:
* If no container has `securityContext.privileged` set to `true`, the resource is allowed. If any container does, the resource is denied from being deployed in the cluster.

A container with no `securityContext` at all is allowed, and so is one with `privileged: false`.

## How this relates to C-0057:
C-0057 checks the same `privileged` field, so anything denied here is denied there too. C-0057 goes further and also denies a container that adds the `SYS_ADMIN` or `ALL` capability, which this policy allows. So a workload that adds capabilities without setting `privileged` is a C-0057 violation and not a C-0193 one.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
