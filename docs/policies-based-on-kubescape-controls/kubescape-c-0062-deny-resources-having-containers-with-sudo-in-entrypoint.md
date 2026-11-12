# Kubescape C-0062: Deny resources having containers with sudo in entrypoint

## Why this policy is required:
Adding sudo to a container entry point command may escalate process privileges and allow access to forbidden resources.

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
This Policy checks the `command` field of every container, init container, and ephemeral container (added with `kubectl debug`). If any entry in a container's `command` contains `sudo`, the resource is denied from being deployed in the cluster.

The policy reads the `command` field declared in the resource. It does not check `args`, or the entrypoint built into the container image, so a container that gets `sudo` only from `args` or from its image's default entrypoint is not denied.

## A note on `kubectl debug`:
This policy checks every container in the Pod, not only the new debug container. By default, `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers have `sudo` in their `command`, for example because the Pod was created before this policy was bound. Whether the new debug container complies depends on the command you give it after `--`. `--custom` cannot set the command, because kubectl rejects a custom profile that sets `command`.

`kubectl debug --copy-to` instead creates a new Pod that copies the original Pod's containers and, by default, its init containers. This policy checks that new Pod when it is created, so it is denied if any copied container has `sudo` in its `command`.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)