# Kubescape C-0203: Minimize the admission of HostPath volumes

## Why this policy is required:
A container which mounts a `hostPath` volume as part of its specification will have access to the filesystem of the underlying cluster node. The use of `hostPath` volumes may allow containers access to privileged areas of the node filesystem.

There should be at least one admission control policy defined which does not permit containers to mount `hostPath` volumes.

If you need to run containers which require `hostPath` volumes, this should be defined in a separate policy and you should carefully check to ensure that only limited service accounts and users are given permission to use that policy.

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
This Policy checks the volume list in the pod spec of the resource:
* If no volume declares a `hostPath` source, the resource is allowed. If any volume does, the resource is denied from being deployed in the cluster.

A resource with no volumes at all is allowed, and so is one whose volumes are all of some other type such as `emptyDir` or a projected secret.

## How this relates to the other hostPath policies:
* **C-0048** checks the same field in the same way. If you have both bound, they will deny the same resources.
* **C-0045** is narrower. It only denies a `hostPath` volume that is *mounted without* `readOnly: true`. A read only hostPath mount passes C-0045 and is still denied here, since this control is about the volume existing at all rather than about how it is mounted.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
