kubescape-c-0055-linux-hardening
# Kubescape C-0055: Linux Hardening

## Why this policy is required:
In order to reduce the attack surface, it is recommend, when it is possible, to harden your application using security services such as SELinux®, AppArmor®, and seccomp. Starting from Kubernetes version 22, SELinux is enabled by default.

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
This Policy checks if there is `AppArmor` or `Seccomp` or `SELinux` or `Capabilities` are defined in the `securityContext` of container and pod. If none of these fields are defined for both the container and pod in workload, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)