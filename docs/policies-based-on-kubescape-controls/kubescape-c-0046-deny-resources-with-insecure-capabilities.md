# Kubescape C-0046: Deny resources with insecure capabilities

## Why this policy is required:
Giving insecure and unnecessary capabilities for a container can increase the impact of a container compromise.


## Severity Level: High

## Configuration Parameters:
* [insecureCapabilities](https://hub.armosec.io/docs/configuration_parameter_insecurecapabilities)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy compares all the capabilities in every container against a configurable blacklist of [insecureCapabilities](https://hub.armosec.io/docs/configuration_parameter_insecurecapabilities). If there is a match, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)