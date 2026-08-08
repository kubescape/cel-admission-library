# Kubescape C-0081: CVE-2022-24348 Argo CD directory traversal

## Why this policy is required:
CVE-2022-24348 is a supply chain zero day in Argo CD. A path traversal in the Helm chart handling lets an attacker who can craft a chart read files outside the repository, which leads to privilege escalation and information disclosure. It is fixed in 2.1.9 and 2.2.4.

## Severity Level: Medium

## Configuration Parameters:
* Not Configurable

## Resources this policy could be applied to:
* Deployment

## What does this policy do:
This Policy checks every container image in the Deployment, including init containers:
* If the image names `argocd` as its last repository segment and the tag is a three part numeric version in the vulnerable range, the resource is denied from being deployed in the cluster.

The vulnerable range is any `1.x`, any `2.0.x`, `2.1.x` below `2.1.9`, and `2.2.x` below `2.2.4`.

`argocd` has to be a whole repository segment, so `argoproj/argocd:v2.1.8` and a bare `argocd:v2.1.8` are both matched, while an unrelated image such as `myargocd:v1.8.7` is not.

A tag that is not a plain three part number, for example `v2.1` or `v2.1.0-rc1`, is allowed. The policy cannot tell what such a tag resolves to, and guessing would either raise an evaluation error or block valid images.

## Implementing this policy in the Cluster:
[Refer here for using the policy in the cluster](https://github.com/kubescape/cel-admission-library#using-the-library)
