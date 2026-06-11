# Conversion Guide

This guide is for anyone adding a new control to this library or migrating an existing Rego rule from `kubescape/regolibrary` into a CEL `ValidatingAdmissionPolicy`. Read it once before you open your first PR. It assumes you already know the Rego rule you are translating (or the policy you are writing from scratch) and that you have basic Kubernetes admission knowledge.

If you only need a reference for CEL syntax itself, the upstream Kubernetes VAP docs are the right place to look. This guide covers the things that are specific to how this repo is laid out and the traps that keep tripping new contributors.

## 1. What a control looks like in this repo

A single control is five files:

- `controls/C-XXXX/policy.yaml` — the `ValidatingAdmissionPolicy` itself
- `controls/C-XXXX/tests.json` — the test cases for the harness
- `docs/policies-based-on-kubescape-controls/<policy-name>.md` — the human-facing doc
- one new line in `controls/kustomization.yaml` registering the policy
- one new row in the library table in `README.md`

Get all five right or the policy will work locally but fail to register through kustomize, or it will register but not show up in the table.

## 2. The dispatch-by-kind pattern

One policy in this repo typically binds Pod, the workload kinds (Deployment, ReplicaSet, DaemonSet, StatefulSet, Job), and CronJob all together through `matchConstraints`. Each kind needs a different path to reach the container list. So a policy ends up with three expressions that look like this:

```yaml
- expression: "object.kind != 'Pod' || object.spec.containers.all(...)"
- expression: "['Deployment','ReplicaSet','DaemonSet','StatefulSet','Job'].all(kind, object.kind != kind) || object.spec.template.spec.containers.all(...)"
- expression: "object.kind != 'CronJob' || object.spec.jobTemplate.spec.template.spec.containers.all(...)"
```

The `object.kind != 'Pod' || ...` guard at the front looks redundant against `matchConstraints`, but it is not. It is the dispatch mechanism. When a Deployment comes in, the Pod expression short-circuits to `true` through that guard. Without the guard, the Pod expression would try to read `object.spec.containers` on a Deployment object and fail.

Do not remove these guards. If you do, your policy will break on every kind except the one the expression is written for.

## 3. The `variables:` block

The repo ships two styles for the same logic. The older style copies the container walk three times, once per expression. The newer style pulls the walk into a `variables:` block at the top of the policy and references it from each validation:

```yaml
variables:
  - name: containers
    expression: |
      object.kind == 'Pod'
        ? object.spec.containers
            + (has(object.spec.initContainers) ? object.spec.initContainers : [])
            + (has(object.spec.ephemeralContainers) ? object.spec.ephemeralContainers : [])
        : object.kind in ['Deployment','ReplicaSet','DaemonSet','StatefulSet','Job']
          ? object.spec.template.spec.containers
              + (has(object.spec.template.spec.initContainers) ? object.spec.template.spec.initContainers : [])
              + (has(object.spec.template.spec.ephemeralContainers) ? object.spec.template.spec.ephemeralContainers : [])
          : object.kind == 'CronJob'
            ? object.spec.jobTemplate.spec.template.spec.containers
                + (has(object.spec.jobTemplate.spec.template.spec.initContainers) ? object.spec.jobTemplate.spec.template.spec.initContainers : [])
                + (has(object.spec.jobTemplate.spec.template.spec.ephemeralContainers) ? object.spec.jobTemplate.spec.template.spec.ephemeralContainers : [])
            : []
validations:
  - expression: "variables.containers.all(c, ...)"
```

C-0198 and C-0210 are the worked examples. The newer style is what to use for new controls. A bug in the container walk lives in one place instead of three.

If you are migrating an existing control that uses the older copy-paste style and you are already in the file for a Rego-to-CEL migration, convert it to the `variables:` style in the same PR. Do not open a sweep PR that touches every control at once.

### Don't forget init and ephemeral containers

A Pod's security posture includes its init containers and ephemeral containers, not just the main containers list. An attacker who can run an init container with `NET_RAW` has the same surface as one who can run a main container with `NET_RAW`. Your container walk should include all three lists:

```
object.spec.containers
  + (has(object.spec.initContainers) ? object.spec.initContainers : [])
  + (has(object.spec.ephemeralContainers) ? object.spec.ephemeralContainers : [])
```

C-0198, C-0199, C-0200, C-0201, and C-0210 all do this. Some older policies (C-0017, C-0046) only walk the main containers list and miss init containers. That is a known gap and should not be the pattern you copy for new controls.

## 4. `failurePolicy` vs binding `validationActions`

This is the trap. I assumed at one point that flipping a policy's `failurePolicy` from `Fail` to `Ignore` would make a control audit-only. It does not. The two fields control different things.

- `failurePolicy` lives on the policy and governs what happens when CEL fails to evaluate at all (compile error, type error, runtime panic). `Fail` rejects the request, `Ignore` admits it silently.
- `validationActions` lives on the binding and governs what happens when CEL evaluates cleanly to `false`. `[Deny]` rejects the request, `[Audit]` records an audit annotation, `[Warn]` returns a Kubernetes API server warning to the client.

The normal "policy violated" path produces a clean `false`. That is the `validationActions` lever, not the `failurePolicy` lever.

This matters when you migrate an audit-style Rego rule, like C-0026, which alerts on every CronJob rather than denying. The policy YAML on its own cannot express "audit-only." You ship the policy plus a `[Warn]` or `[Audit]` binding alongside it and document the requirement on the policy's doc page. `test-resources/policy-binding-warn.yaml` is the existing example, and the C-0026 doc shows how to call it out.

The general rule: `validationActions` is an operator-by-binding decision, and the library only needs to ship a non-`[Deny]` binding when `[Deny]` would block legitimate, compliant resources. C-0026 is the sole control in the current library where that applies. For every other control in this repo, the default `[Deny]` binding is the right shipped default, and the operator can override per cluster if they want audit semantics.

## 5. When `paramKind` makes sense

Use `paramKind` only when the control has tunable knobs that an operator should be able to override per cluster. C-0046 is the example to look at. It accepts a `ControlConfiguration` parameter holding a list of insecure capabilities so different orgs can decide what counts as insecure for them.

Do not add a `paramKind` for a binary policy. C-0199 deny-NET_RAW has nothing to tune. C-0280 deny-CSR-approval has nothing to tune. Adding a `paramKind` for completeness is dead weight that the operator has to populate with an empty config or the policy refuses to admit.

## 6. The test harness

A test case in `tests.json` has five fields:

```json
{
    "name": "human readable description",
    "template": "pod.yaml",
    "binding_template": "policy-binding-warn.yaml",
    "expected": "warn",
    "field_change_list": ["spec.containers.[0].securityContext.runAsUser=0"]
}
```

- `template` points to a YAML in `test-resources/` which the harness will use as the input object.
- `field_change_list` (optional) patches fields on that input before the harness applies it. The index syntax is `.[0]`, as in `spec.template.spec.containers.[0].securityContext.capabilities.drop=["ALL"]`.
- `expected` is one of `pass`, `fail`, `warn`. `pass` means the apply succeeds with no policy match. `fail` means the apply is denied by this policy. `warn` means the apply succeeds and this policy emits a Kubernetes warning to the client.
- `binding_template` (optional, default `policy-binding.yaml`) picks which binding the harness applies the policy under. Use `policy-binding-warn.yaml` for audit-style controls and let `expected` be `warn`.

Run the harness for a single control against any VAP-capable cluster (Kubernetes 1.30 or later) with:

```bash
cd controls/C-XXXX
python3 ../../scripts/run-control-tests.py
```

The harness creates a `test-namespace`, applies the policy, the binding, and a parameter object built from `test-resources/default-control-configuration.yaml`. The parameter object is applied for every test, even for controls without a `paramKind`, because the binding's `parameterNotFoundAction: Deny` would otherwise reject every request. Treat it as harness plumbing, not as a per-control concern. The harness then dry-run-applies each test object and cleans up after itself.

If your cluster doesn't list `validatingadmissionpolicies` under `kubectl api-resources --api-group=admissionregistration.k8s.io`, VAP is not enabled. Upgrade to Kubernetes 1.30 or later, or spin up a fresh kind cluster on a 1.30+ image.

## 7. Writing the doc page

Every control gets a Markdown page under `docs/policies-based-on-kubescape-controls/<policy-name>.md` matching the policy's `metadata.name`. The page covers why the policy exists, severity, configuration parameters, the resources it applies to, what it does, and how to install it. Existing pages are good templates.

If the control needs a non-default binding (any audit-style control falls in this bucket), say so loudly on the doc page. Reference the example binding file the user should apply, and warn them that the default `[Deny]` binding shipped in `test-resources/policy-binding.yaml` is not safe for the control.

## 8. Notes for migrating from Rego

A few practical CEL versus Rego gotchas worth keeping in mind:

- CEL has no `default` keyword. Use `has(x.y) ? x.y : <fallback>` to guard optional fields.
- CEL has no rule composition the way Rego does. You write one expression per `validation:` entry. Shared logic goes into the `variables:` block.
- CEL's `.all(...)` and `.exists(...)` replace Rego's universal and existential quantifiers.
- CEL has no `print`. Debugging happens by reading the API server reject reason or warning.
- The Rego rule's input object is whatever the Rego policy receives. The CEL policy's `object` is the Kubernetes resource being admitted, with the schema you would see if you ran `kubectl get -o yaml` on it. Most of the time the migration is straightforward, but if the Rego rule mutates or accumulates state across multiple input objects, the CEL version usually needs to be rewritten to evaluate a single object at a time.

## 9. Before you open the PR

A short checklist:

- The five files from section 1 all exist and are wired together.
- The dispatch guards from section 2 are in place if your policy binds multiple kinds.
- New controls use the `variables:` style from section 3 and walk init and ephemeral containers.
- If the control is audit-style, you have shipped or pointed at a `[Warn]` or `[Audit]` binding and the doc page says so (section 4).
- `paramKind` is present only if the control has real tunable knobs (section 5).
- The harness passes locally against a VAP-capable cluster (section 6).
- The doc page is filled out (section 7).
- For migrations, the CEL behaviour matches the Rego behaviour on at least the pass and fail fixtures from the Rego rule's existing tests.
