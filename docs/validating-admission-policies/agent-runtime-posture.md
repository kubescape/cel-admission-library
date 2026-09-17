# Agent runtime posture admission policies

These policies validate fields on Agent Sandbox `Sandbox` and `SandboxTemplate`
resources using the `v1beta1` APIs served by Agent Sandbox v1.0 and later. They
also validate Agent Substrate `WorkerPool` resources, which continue to use the
separate `ate.dev/v1alpha1` API. The control IDs match the
AgentRuntimeHardening framework in regolibrary:

| Control | Admission evidence |
| --- | --- |
| C-0297 | Sandbox/Template RuntimeClass selection |
| C-0309 | Sandbox/Template service account token automounting (`v1beta1`) |
| C-0311 | Sandbox/Template CPU and memory limits, including init containers |
| C-0312 | Sandbox/Template images and WorkerPool `spec.workerImage`, with exact lowercase SHA-256 pins |
| C-0313 | Registry allowlisting for the same image fields |
| C-0314 | SandboxTemplate managed networking |

C-0297 reuses the existing Rego control and `hardenedSandboxRuntimeClasses`
configuration (default: `gvisor`). Add `kata` to that shared list if approved.
Missing/empty runtime and image registry allowlists disable their respective
checks. A binding without `paramRef` also disables these configurable checks.
This allows older configurations to keep working without CEL evaluation errors.
A `paramRef` pointing at a nonexistent configuration is still governed by its
`parameterNotFoundAction`.

When `imageRepositoryAllowList` includes `docker.io`, unqualified images such as
`nginx`, `nginx:1.27`, `nginx@sha256:...`, and `library/nginx` are allowed by the
registry check. Explicit registry hosts and ports must be separately allowlisted.
The digest policy still requires exact pins, independently of registry checks.

Direct `Sandbox` resources must explicitly set `automountServiceAccountToken:
false`. `SandboxTemplate` resources may omit the field to retain the controller's
secure default, but must not set it to `true`.

`networkPolicyManagement: Managed` blocks private/internal destinations by
default while allowing public internet. It does not establish a strict egress
allowlist. Omitted or null management uses the API default.

The WorkerPool field was verified against
[WorkerPoolSpec](https://github.com/agent-substrate/substrate/blob/a9c1bd389403af59520e419d3884d447cf40edd2/pkg/api/v1alpha1/workerpool_types.go).
ActorTemplate is an [ATE protobuf resource](https://github.com/agent-substrate/substrate/blob/a9c1bd389403af59520e419d3884d447cf40edd2/pkg/proto/ateapipb/ateapi.proto),
not a Kubernetes CRD, so it is not targeted by these policies or represented by
an invented test CRD. Actor checks require a supported scanner integration first.

`SandboxClaim` and `SandboxWarmPool` are not matched directly because the
posture fields checked here live on the referenced `SandboxTemplate` and the
resulting `Sandbox`.

The policies do not use `spec.matchConditions`, contact image registries, verify
signatures, or make cross-resource IAM claims. Registry and digest checks
validate names and syntax only.

Start with `agent-runtime-posture-bindings.yaml`, which uses `Warn` and `Audit`.
Change a binding to `Deny` after observing and testing the policy in the target
cluster.

## Tests

Run `scripts/run-all-control-tests.sh` only against a disposable test cluster.
The runner refuses pre-existing Agent test CRDs before making changes. It uses
`kubectl create`, labels each CRD with a unique run ID, waits for `Established`,
and cleans up only that run's CRDs on normal exit, failure, or interruption.
It never applies test schemas over installed Agent Sandbox or Substrate CRDs.
The rest of the suite also uses test namespaces and admission policies.
