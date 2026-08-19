# Kubescape C-0020: Deny resources having volumes with potential access to known cloud credentials

## Why this policy is required:
When a cluster is deployed in the cloud, in some cases attackers can leverage their access to a container in the cluster to gain cloud credentials. This control determines if any workload contains a volume with potential access to cloud credentials.

## Severity Level: Medium

## Configuration Parameters:
* [cloudProvider](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks every `hostPath` volume in the pod spec against a list of paths that hold cloud credentials on the node. The list depends on the configured `cloudProvider`:

* `eks`: `/.aws/`, `/.aws/config/`, `/.aws/credentials/`
* `aks`: `/etc/`, `/etc/kubernetes/`, `/etc/kubernetes/azure.json`, `/.azure/`, `/.azure/credentials/`
* `gke`: `/.config/gcloud/`, `/.config/`, `/gcloud/`, `/gcloud/application_default_credentials.json`, `/.config/gcloud/application_default_credentials.json`

A volume that is not a `hostPath`, or a `hostPath` whose path is not one of those, is allowed. A resource with no volumes is allowed.

## Configuring cloudProvider:
Only the provider matching `cloudProvider` is checked. The shipped `basic-control-configuration.yaml` sets it to the empty string, which matches no provider, so **the policy allows everything until you configure it**. Set it to `eks`, `aks` or `gke` to match the cluster you are running on.

That default is deliberate. The paths for one provider are ordinary locations on another, `/etc/` under `aks` most obviously, so guessing a provider would deny normal workloads on a cluster running somewhere else.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
