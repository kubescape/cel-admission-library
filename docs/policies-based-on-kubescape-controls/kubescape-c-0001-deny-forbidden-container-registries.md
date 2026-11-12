# Kubescape C-0001: Deny Forbidden Container Registries

## Why this policy is required:
Running a compromised image in a cluster can compromise the cluster. Attackers who get access to a private registry
can plant their own compromised images in the registry. The latter can then be pulled by a user. In addition, users often
use untrusted images from public registries (such as Docker Hub) that may be malicious. Building images based on untrusted base
images can also lead to similar results.

## Severity Level: High

## Configuration Parameters:
* [untrustedRegistries](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#untrustedregistries)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks if the image used by any container, init container, or ephemeral container (added with `kubectl debug`) is from the configured [untrustedRegistries](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#untrustedregistries). If it finds any such instance, the resource is
denied from being deployed in the cluster.

## A note on `kubectl debug`:
This policy checks every container in the Pod, not only the new debug container. By default, `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers use a forbidden registry, for example because the Pod was created before this policy was bound. Whether the new debug container complies depends on the image you pass with `--image`. `--custom` cannot change the image, because kubectl rejects a custom profile that sets `image`.

`kubectl debug --copy-to` instead creates a new Pod that copies the original Pod's containers and, by default, its init containers. This policy checks that new Pod when it is created, so it is denied if any copied container uses a forbidden registry.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)