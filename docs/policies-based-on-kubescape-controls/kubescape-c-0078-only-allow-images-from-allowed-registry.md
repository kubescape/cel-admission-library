# Kubescape C-0078: Deny resources with images not from allowed registry

## Why this policy is required:
If attackers get access to the cluster, they can re-point kubernetes to a compromized container repository. This control is intended to ensure that all the container images are taken from the authorized repositories only.

## Severity Level: Medium

## Configuration Parameters:
* [imageRepositoryAllowList](https://hub.armosec.io/docs/configuration_parameter_imagerepositoryallowlist)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks that all the containers in the resource are using images from the [imageRepositoryAllowList](https://hub.armosec.io/docs/configuration_parameter_imagerepositoryallowlist). If not, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)