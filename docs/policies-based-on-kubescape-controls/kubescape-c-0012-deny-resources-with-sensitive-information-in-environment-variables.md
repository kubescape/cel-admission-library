# Kubescape C-0012: Deny if application credentials found in configuration files

## Why this policy is required:
Developers store secrets in the Kubernetes configuration files, such as environment variables in the pod configuration. Such behavior is commonly seen in clusters that are monitored by Azure Security Center. Attackers who have access to those configurations, by querying the API server or by accessing those files on the developer’s endpoint, can steal the stored secrets and use them.Note, this control is configurable. See below the details.

## Severity Level: High

## Configuration Parameters:
* [sensitiveValues](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivevalues)
* [sensitiveValuesAllowed](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivevaluesallowed)
* [sensitiveKeyNames](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivekeynames)
* [sensitiveKeyNamesAllowed](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivekeynames)

## Resources this policy could be applied to:
* ConfigMap
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
### This Policy checks for every container (regular, init, and ephemeral containers added with `kubectl debug`) in the resource:
* If pod has sensitive information in environment variables, by using list of known sensitive key names and values.

### This Policy checks for every configMap in the resource:
* If configMap contains sensitive information.

## A note on `kubectl debug`:
This policy checks every container in the Pod, not only the new debug container. `kubectl debug` adds the debug container by updating the existing Pod, so the request is denied if any of the Pod's existing containers have sensitive environment variables, for example because the Pod was created before this policy was bound. `--custom` only makes the new debug container compliant. It does nothing for the Pod's existing containers.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)