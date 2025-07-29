# Kubescape C-0077: Deny resources without configured list of k8s common labels not set.

## Why this policy is required:
Kubernetes common labels help manage and monitor Kubernetes cluster using different tools such as kubectl, dashboard and others in an interoperable way. Refer to [this link](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) for more information.

## Severity Level: Low

## Configuration Parameters:
* [k8sRecommendedLabels]( https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#k8srecommendedlabels)

## Resources this policy could be applied to:
* CronJob
* DaemonSet
* Deployment
* Job
* Pod
* ReplicaSet
* StatefulSet

## What does this policy do:
This Policy checks if resource sets the labels defined in the configurable [k8sRecommendedLabels](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#k8srecommendedlabels). If not set, the resource is denied from being deployed in the cluster.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)