# Kubescape C-0204: Minimize the admission of containers which use HostPorts

## Why this policy is required:
Host ports connect containers directly to the host's network. This can bypass controls such as network policy.

There should be at least one admission control policy defined which does not permit containers which require the use of HostPorts.

If you need to run containers which require HostPorts, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks every container in the resource, including init containers and ephemeral containers:
* If no container declares a port with a `hostPort`, the resource is allowed. If any container does, the resource is denied from being deployed in the cluster.

A container with no `ports` at all is allowed, and so is one that declares only `containerPort`.

`hostPort: 0` is treated as allowed. `HostPort` is a plain `int32` in the Kubernetes API type rather than a pointer, so a manifest carrying an explicit zero means the same thing as leaving the field out: no port is claimed on the node.

## How this relates to C-0044:
C-0044 checks the same field, and for an ordinary workload the two agree. They differ in two places:
* This policy walks init containers and ephemeral containers as well as `containers`. C-0044 only looks at `containers`, so a `hostPort` on an init container passes it and is denied here.
* C-0044 denies on the presence of the field, so it also denies an explicit `hostPort: 0`. This policy allows that.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
