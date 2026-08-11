# Kubescape C-0207: Prefer using secrets as files over secrets as environment variables

## Why this policy is required:
A Secret injected as an environment variable is readable by anything that can read the process environment. It shows up in `kubectl describe` output, it gets inherited by every child process the container spawns, and it often ends up in crash dumps and logs. Mounting the Secret as a file keeps it out of all of those places and lets you rotate it without restarting the pod.

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
This Policy checks every container in the resource, including init containers and, for a Pod, ephemeral containers:
* If any environment variable takes its value from `valueFrom.secretKeyRef`, the resource is denied from being deployed in the cluster.

Environment variables sourced from a ConfigMap, from a field reference or from a plain value are not affected.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
