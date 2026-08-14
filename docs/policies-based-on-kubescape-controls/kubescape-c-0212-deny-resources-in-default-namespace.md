# Kubescape C-0212: The default namespace should not be used

## Why this policy is required:
The `default` namespace is where everything lands when nobody says otherwise. That makes it the one namespace you cannot write a meaningful RBAC rule about, because it holds unrelated things from unrelated teams. The same goes for ResourceQuota, LimitRange and most NetworkPolicy setups: they are namespace scoped, so a workload sitting in `default` alongside everything else gets no boundary of its own. Putting each application in a namespace made for it is what makes those controls mean anything.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* CSIStorageCapacity
* ConfigMap
* CronJob
* DaemonSet
* Deployment
* EndpointSlice
* Endpoints
* HorizontalPodAutoscaler
* Ingress
* Job
* Lease
* PersistentVolumeClaim
* Pod
* PodDisruptionBudget
* PodTemplate
* ReplicaSet
* ReplicationController
* Role
* RoleBinding
* Secret
* Service
* ServiceAccount
* StatefulSet

## What does this policy do:
This Policy reads `metadata.namespace` on the resource:
* If it is `default`, the resource is denied from being deployed in the cluster.
* If it is missing, the resource is denied too. A manifest with no namespace goes to `default` when it is applied, so leaving it out is the same thing as asking for `default`.

The second case only ever shows up when the manifest is read from a file, for example during a Kubescape scan. At live admission the apiserver has already filled the field in before any policy runs.

## How this relates to C-0061:
[C-0061](/docs/policies-based-on-kubescape-controls/kubescape-c-0061-deny-workloads-in-default-namespace.md) asks the same question, but only of the seven workload kinds. This one asks it of 23 kinds, so a ConfigMap, a Role or an Ingress in `default` is caught here and not there. They are separate CIS recommendations and both exist upstream, so both exist here. If you bind both, expect a workload in `default` to be reported twice.

## Read this before binding it:
`default` is where a lot of ordinary cluster bootstrap happens, so binding this one with `validationActions: [Deny]` blocks more than you might expect, including updates to objects that were already living in `default` before you installed the policy. `[Warn]` or `[Audit]` is the safer starting point. The library ships policies only and no bindings, so the enforcement level is yours to pick at install time.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
