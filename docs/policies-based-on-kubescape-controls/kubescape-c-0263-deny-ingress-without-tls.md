# Kubescape C-0263: Ingress uses TLS

## Why this policy is required:
An Ingress with no TLS configuration serves its traffic over plaintext HTTP. Anything on the network path can read or modify the requests and responses, including credentials and session tokens.

## Severity Level: High

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Ingress

## What does this policy do:
This Policy checks the Ingress:
* If `spec.tls` is missing, or present but empty, the Ingress is denied from being deployed in the cluster. An empty `tls` list configures no TLS at all, so it is treated the same as a missing one.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
