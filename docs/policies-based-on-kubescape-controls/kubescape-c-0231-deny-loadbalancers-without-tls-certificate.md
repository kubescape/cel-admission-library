# Kubescape C-0231: Encrypt traffic to HTTPS load balancers with TLS certificates

## Why this policy is required:
A Service of type LoadBalancer that listens on 443 without an SSL certificate configured lacks frontend TLS termination.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Service

## What does this policy do:
This Policy checks Services of type `LoadBalancer` that serve port 443:
* If the annotation `service.beta.kubernetes.io/aws-load-balancer-ssl-cert` is missing or empty, the Service is denied from being deployed in the cluster.

Services of any other type, and LoadBalancers that do not serve 443, are not affected.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
