# Kubescape C-0234: Consider external secret storage

## Why this policy is required:
Kubernetes Secrets are only base64 encoded, they sit in etcd, and anything with read access to the namespace can usually read them. An external secret store (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager and so on) keeps the secret material outside the cluster, authenticates every read, records who read what, and lets you rotate a secret without touching the workload. The secrets-store CSI driver is how a workload consumes one of those stores: it mounts the secret as a file at runtime instead of taking it from an in-cluster Secret object.

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
This Policy looks at the volumes of the resource, which for a workload means the volumes of its pod template:
* If none of them is a `secrets-store.csi.k8s.io` CSI volume carrying a non-empty `csi.volumeAttributes.secretProviderClass`, the resource is denied from being deployed in the cluster.

A resource with no volumes at all is treated the same as one whose volumes are all ordinary: neither reads secrets from an external store.

The driver name is checked, not just the attribute. Another CSI driver that happens to expose an attribute called `secretProviderClass` is not the secrets-store driver and does not satisfy this control. An empty value does not satisfy it either.

## Read this before binding it:
This policy is inverted compared to almost everything else in the library. It does not deny a resource for doing something dangerous, it denies a resource for not doing something good. That means it fires on nearly every workload in a normal cluster, because nearly every workload does not use the secrets-store CSI driver.

That is deliberate. CIS phrases this recommendation as "consider", so it is advisory rather than a hard rule, and the Kubescape control it comes from behaves the same way.

If you bind this policy, think carefully before using `validationActions: [Deny]`. `[Warn]` or `[Audit]` is usually what you want: it surfaces the workloads that are still on in-cluster Secrets without blocking every deployment in the cluster on day one. The library ships policies only and no bindings, so this is entirely your call at install time.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
