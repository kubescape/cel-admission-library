# Kubescape C-0231: Encrypt traffic to HTTPS load balancers with TLS certificates

## Why this policy is required:
A Service of type LoadBalancer that listens on 443 without an SSL certificate configured is not terminating TLS anywhere. Clients think they are talking HTTPS, but the traffic between the load balancer and the backend is plaintext.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Service

## What does this policy do:
This Policy checks Services of type `LoadBalancer` that serve port 443:
* If no annotation key starts with `service.beta.kubernetes.io/aws-load-balancer-ssl-cert`, the Service is denied from being deployed in the cluster.

The match is on the annotation key prefix rather than an exact key, because the AWS load balancer annotation family has suffixed variants.

Services of any other type, and LoadBalancers that do not serve 443, are not affected.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
