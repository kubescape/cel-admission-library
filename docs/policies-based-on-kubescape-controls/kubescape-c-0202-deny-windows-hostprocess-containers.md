# Kubescape C-0202: Minimize the admission of Windows HostProcess Containers

## Why this policy is required:
A Windows container making use of the `hostProcess` flag can interact with the underlying Windows cluster node. As per the Kubernetes documentation, this provides "privileged access" to the Windows node.

Where Windows containers are used inside a Kubernetes cluster, there should be at least one admission control policy which does not permit `hostProcess` Windows containers.

If you need to run Windows containers which require `hostProcess`, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks `securityContext.windowsOptions.hostProcess` in two places, and denies the resource if either one is `set to true`:
* On the pod security context, where it becomes the default for every container in the pod.
* On any individual container, including init containers and ephemeral containers.

A `windowsOptions` block that sets something else, such as `runAsUserName`, and leaves `hostProcess` out is allowed. So is `hostProcess` explicitly `set to false`.

These are written as two separate checks rather than one. `hostProcess` on the pod security context and `hostProcess` on a container are different things to fix, and keeping them apart means the reported field is the one you actually have to edit.

## A note on what a live cluster will let you send:
The API server has its own rules about `hostProcess` that run before any admission policy does. A pod that sets it must also set `hostNetwork: true`, and if any container is a HostProcess container then all of them have to be. So the mixed case, one HostProcess container next to a normal one, never reaches this policy on a real cluster. It can still appear in a manifest scanned from a file, which is why the container check walks every container rather than stopping at the first.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
