# Kubescape C-0198: Deny root containers

## Why this policy is required:
Running containers as root (UID 0) grants full privileges inside the container, increasing the impact of a container breakout. Explicitly setting `runAsUser: 0` should be blocked, and containers should run with a non-root UID or inherit a non-root UID from the pod security context.

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
This Policy checks every container, init container, and ephemeral container (added with `kubectl debug`) for an explicit or inherited `runAsUser` of 0. It first checks if the container has `securityContext.runAsUser` set; if so, that value must not be 0. If the container does not set its own `runAsUser`, the pod-level `securityContext.runAsUser` is checked instead. If either evaluates to 0, the resource is denied.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
