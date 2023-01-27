# Kubescape C-0057: Deny resources with privileged container

## Why this policy is required:
A privileged container is a container that has all the capabilities of the host machine, which lifts all the limitations regular containers have. Practically, this means that privileged containers can do almost every action that can be performed directly on the host. Attackers who gain access to a privileged container or have permissions to create a new privileged container (by using the compromised pod’s service account, for example), can get access to the host’s resources.


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
This Policy checks for every container in the resource:
* If `securityContext.privileged` is not set or set to false.
* If `securityContext.capabilities.add` does not contain `SYS_ADM` capability.

. If any of the above two checks fail, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)