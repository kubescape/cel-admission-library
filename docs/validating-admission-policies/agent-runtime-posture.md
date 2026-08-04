# Agent runtime posture admission policies

These policies validate self-contained fields on Agent Sandbox `Sandbox` and
`SandboxTemplate` resources. They cover RuntimeClass selection, service account
token automounting, container limits, exact SHA-256 image pins, configured image
registries, and managed networking.

The policies intentionally do not use `spec.matchConditions`, contact image
registries, verify signatures, or make cross-resource egress and IAM claims.
Registry and digest checks validate syntax and names only.

`networkPolicyManagement: Managed` blocks private and internal destinations by
default while allowing public internet. It is useful isolation, but it is not a
strict default-deny egress allowlist. The managed-networking policy and message
preserve that distinction.

Start with the bindings in
`agent-runtime-posture-bindings.yaml`, which use `Warn` and `Audit`. Change a
binding to `Deny` only after the relevant policy has been observed and tested in
the target cluster.
