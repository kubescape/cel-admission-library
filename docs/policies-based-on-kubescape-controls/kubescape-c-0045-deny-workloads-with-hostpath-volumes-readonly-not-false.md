# Kubescape C-0045: Deny resources with hostPath volumes is not read-only

## Why this policy is required:
hostPath volume mounts a directory or a file from the host to the container. Attackers who have permissions to create a new container in the cluster may create one with a writable hostPath volume and gain persistence on the underlying host. For example, the latter can be achieved by creating a cron job on the host.

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
This Policy is checking in POD spec if there is a `hostPath` volume, if it has the section `mount.readOnly == false` (or doesn’t exist). If the above check fails, the resource is denied from being deployed into the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)