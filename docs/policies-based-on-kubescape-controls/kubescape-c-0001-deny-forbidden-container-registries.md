# Kubescape C-0001: Deny Forbidden Container Registries

## Why this policy is required:
Running a compromised image in a cluster can compromise the cluster. Attackers who get access to a private registry
can plant their own compromised images in the registry. The latter can then be pulled by a user. In addition, users often
use untrusted images from public registries (such as Docker Hub) that may be malicious. Building images based on untrusted base
images can also lead to similar results.

## Severity Level: High

## Configuration Parameters:
* [untrustedRegistries](https://hub.armosec.io/docs/configuration_parameter_untrustedregistries)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks if the image used by any container is from the configured [untrustedRegistries](https://hub.armosec.io/docs/configuration_parameter_untrustedregistries). If it finds any such instance, the resource is
denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)