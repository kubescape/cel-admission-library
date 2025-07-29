# Kubescape Validating Admission Policy library

This is a library of policies based on [Kubescape controls](https://kubescape.io/docs/controls/) ready for use with [Kubernetes Validating Admission Policies](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). In this library, Kubescape controls have been re-implemented in [CEL](https://github.com/google/cel-spec/) for your convenience.

## Using the library

Kubernetes Validating Admission Policy (or *VAP*) feature was released as a GA feature in version 1.30 and it is a releatively new feature (this library supports alpha and beta versions as well). Before you start playing with it, make sure you have a cluster that supports this feature. Look [here](docs/validating-admission-policies/README.md) for _how to _set up_ a playground_ even for pre-1.30 versions.*

Install latest the release of the library (`v1` version of *VAP*):
```bash
# Install configuration CRD
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/policy-configuration-definition.yaml
# Install basic configuration
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/basic-control-configuration.yaml
# Install policies
kubectl apply -f https://github.com/kubescape/cel-admission-library/releases/latest/download/kubescape-validating-admission-policies.yaml
```

You're good to start to use it 😎

You can apply policies to objects, for example, to apply control [C-0016](hhttps://kubescape.io/docs/controls/c-0016/) (deny `allowPrivilegeEscalation` on containers) on workloads in the namespace with label `policy=enforced` just run this:

```bash
# Creating a binding
kubectl apply -f - <<EOT
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicyBinding
metadata:
  name: c0016-binding
spec:
  policyName: kubescape-c-0016-allow-privilege-escalation
  paramRef:
    name: basic-control-configuration
    parameterNotFoundAction: Deny
  validationActions:
  - Deny
  matchResources:
    namespaceSelector:
      matchLabels:
        policy: enforced
EOT
# Creating a namespace for running the example
kubectl create namespace policy-example
kubectl label namespace policy-example policy=enforced
# The next line should fail
kubectl -n policy-example run nginx --image=nginx --restart=Never
```

## Library items
| Control ID | Name | Policy name | Configuration parameter |
| --- | --- | --- | --- |
| [C-0001](https://kubescape.io/docs/controls/c-0001/) | Forbidden Container Registries | [kubescape-c-0001-deny-forbidden-container-registries](/docs/policies-based-on-kubescape-controls/kubescape-c-0001-deny-forbidden-container-registries.md) | [untrustedRegistries](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#untrustedregistries) |
| [C-0009](https://kubescape.io/docs/controls/c-0009/) | Resource limits | [kubescape-c-0009-deny-resources-with-memory-or-cpu-limit-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0009-deny-resources-with-memory-or-cpu-limit-not-set.md) | not configurable |
| [C-0012](https://kubescape.io/docs/controls/c-0012/) | Applications credentials in configuration files | [kubescape-c-0012-deny-resources-with-sensitive-information-in-environment-variables](/docs/policies-based-on-kubescape-controls/kubescape-c-0012-deny-resources-with-sensitive-information-in-environment-variables.md) | [sensitiveValues](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivekeynames), [sensitiveValuesAllowed](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivevaluesallowed), [sensitiveKeyNames](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivekeynames), [sensitiveKeyNamesAllowed](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#sensitivekeynames) |
| [C-0013](https://kubescape.io/docs/controls/c-0013/) | Non-root containers | [kubescape-c-0013-deny-if-container-runs-as-root](/docs/policies-based-on-kubescape-controls/kubescape-c-0013-deny-if-container-runs-as-root.md) | not configurable | 
| [C-0016](https://kubescape.io/docs/controls/c-0016/) | Allow privilege escalation | [kubescape-c-0016-allow-privilege-escalation](/docs/policies-based-on-kubescape-controls/kubescape-c-0016-allow-privilege-escalation.md) | not configurable |
| [C-0017]( https://kubescape.io/docs/controls/c-0017/) | Immutable container filesystem | [kubescape-c-0017-deny-resources-with-mutable-container-filesystem](/docs/policies-based-on-kubescape-controls/kubescape-c-0017-deny-resources-with-mutable-container-filesystem.md) | not configurable |
| [C-0018](https://kubescape.io/docs/controls/c-0018/) | Configured readiness probe | [kubescape-c-0018-deny-resources-without-configured-readiness-probes](/docs/policies-based-on-kubescape-controls/kubescape-c-0018-deny-resources-without-configured-readiness-probes.md) | not configurable |
| [C-0020](https://kubescape.io/docs/controls/c-0020/) | Mount service principal | [kubescape-c-0020-deny-resources-having-volumes-with-potential-access-to-known-cloud-credentials](/docs/policies-based-on-kubescape-controls/kubescape-c-0020-deny-resources-having-volumes-with-potential-access-to-known-cloud-credentials.md) | [cloudProvider](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/) |
| [C-0034](https://kubescape.io/docs/controls/c-0034/) | Automatic mapping of service account | [kubescape-c-0034-deny-resources-with-automount-service-account-token-enabled](/docs/policies-based-on-kubescape-controls/kubescape-c-0034-deny-resources-with-automount-service-account-token-enabled.md) | not configurable |
| [C-0038](https://kubescape.io/docs/controls/c-0038/) | Host PID/IPC privileges | [kubescape-c-0038-deny-resources-with-host-ipc-or-pid-privileges](/docs/policies-based-on-kubescape-controls/kubescape-c-0038-deny-resources-with-host-ipc-or-pid-privileges.md) | not configurable |
| [C-0041](https://kubescape.io/docs/controls/c-0041/) | HostNetwork access | [kubescape-c-0041-deny-resources-with-host-network-access](/docs/policies-based-on-kubescape-controls/kubescape-c-0041-deny-resources-with-host-network-access.md) | not configurable |
| [C-0042](https://kubescape.io/docs/controls/c-0042/) | SSH server running inside container | [kubescape-c-0042-deny-resources-with-ssh-server-running](/docs/policies-based-on-kubescape-controls/kubescape-c-0042-deny-resources-with-ssh-server-running.md) | not configurable |
| [C-0044](https://kubescape.io/docs/controls/c-0044/) | Container hostPort | [kubescape-c-0044-deny-resources-with-host-port](/docs/policies-based-on-kubescape-controls/kubescape-c-0044-deny-resources-with-host-port.md) | not configurable |
| [C-0045](https://kubescape.io/docs/controls/c-0045/) | Writable hostPath mount | [kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false](/docs/policies-based-on-kubescape-controls/kubescape-c-0045-deny-workloads-with-hostpath-volumes-readonly-not-false.md) | not configurable |
| [C-0046](https://kubescape.io/docs/controls/c-0046/) | Insecure capabilities | [kubescape-c-0046-deny-resources-with-insecure-capabilities](/docs/policies-based-on-kubescape-controls/kubescape-c-0046-deny-resources-with-insecure-capabilities.md) | [insecureCapabilities](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#insecurecapabilities) |
| [C-0048](https://kubescape.io/docs/controls/c-0048/) | HostPath mount | [kubescape-c-0048-deny-workloads-with-hostpath-mounts](/docs/policies-based-on-kubescape-controls/kubescape-c-0048-deny-workloads-with-hostpath-mounts.md) | not configurable |
| [C-0050](https://kubescape.io/docs/controls/c-0050/) | Resources CPU limit and request | [kubescape-c-0050-deny-resources-with-cpu-limit-or-request-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0050-deny-resources-with-cpu-limit-or-request-not-set.md) | [cpuLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_min) | 
| [C-0055](https://kubescape.io/docs/controls/c-0055/) | Linux hardening | [kubescape-c-0055-linux-hardening](/docs/policies-based-on-kubescape-controls/kubescape-c-0055-linux-hardening.md) | not configurable |
| [C-0056](https://kubescape.io/docs/controls/c-0056/) | Configured liveness probe | [kubescape-c-0056-deny-resources-without-configured-liveliness-probes](/docs/policies-based-on-kubescape-controls/kubescape-c-0056-deny-resources-without-configured-liveliness-probes.md) | not configurable |
| [C-0057](https://kubescape.io/docs/controls/c-0057/) | Privileged container | [kubescape-c-0057-privileged-container-denied](/docs/policies-based-on-kubescape-controls/kubescape-c-0057-privileged-container-denied.md) | not configurable |
| [C-0061](https://kubescape.io/docs/controls/c-0061/) | Pods in default namespace | [kubescape-c-0061-deny-workloads-in-default-namespace](/docs/policies-based-on-kubescape-controls/kubescape-c-0061-deny-workloads-in-default-namespace.md) | not configurable |
| [C-0062](https://kubescape.io/docs/controls/c-0062/) | Sudo in container entrypoint | [kubescape-c-0062-deny-resources-having-containers-with-sudo-in-entrypoint](/docs/policies-based-on-kubescape-controls/kubescape-c-0062-deny-resources-having-containers-with-sudo-in-entrypoint.md) | not configurable |
| [C-0073](https://kubescape.io/docs/controls/c-0073/) | Naked PODs | [kubescape-c-0073-deny-naked-pods](/docs/policies-based-on-kubescape-controls/kubescape-c-0073-deny-naked-pods.md) | not configurable |
| [C-0074](https://kubescape.io/docs/controls/c-0074/) | Containers mounting Docker socket | [kubescape-c-0074-resources-mounting-docker-socket-denied](/docs/policies-based-on-kubescape-controls/kubescape-c-0074-resources-mounting-docker-socket-denied.md) | not configurable |
| [C-0075](https://kubescape.io/docs/controls/c-0075/) | Image pull policy on latest tag | [kubescape-c-0075-deny-resources-with-image-pull-policy-not-set-to-always-for-latest-tag](/docs/policies-based-on-kubescape-controls/kubescape-c-0075-deny-resources-with-image-pull-policy-not-set-to-always-for-latest-tag.md) | not configurable |
| [C-0076](https://kubescape.io/docs/controls/c-0076/) | Label usage for resources | [kubescape-c-0076-deny-resources-without-configured-list-of-labels-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0076-deny-resources-without-configured-list-of-labels-not-set.md) | [recommendedLabels](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#recommendedlabels) |
| [C-0077](https://kubescape.io/docs/controls/c-0077/) | K8s common labels usage | [kubescape-c-0077-deny-resources-without-configured-list-of-k8s-common-labels-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0077-deny-resources-without-configured-list-of-k8s-common-labels-not-set.md) | [k8sRecommendedLabels](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#k8srecommendedlabels) |
| [C-0078](https://kubescape.io/docs/controls/c-0078/) | Images from allowed registry | [kubescape-c-0078-only-allow-images-from-allowed-registry](/docs/policies-based-on-kubescape-controls/kubescape-c-0078-only-allow-images-from-allowed-registry.md) | [imageRepositoryAllowList](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#imagerepositoryallowlist) |
| [C-0268](https://kubescape.io/docs/controls/c-0268/) | Ensure CPU requests are set | [kubescape-c-0268-deny-resources-with-cpu-request-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0268-deny-resources-with-cpu-request-not-set.md) | [cpuRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_request_min) |
| [C-0269](https://kubescape.io/docs/controls/c-0269/) | Ensure memory requests are set | [kubescape-c-0269-deny-resources-with-memory-request-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0269-deny-resources-with-memory-request-not-set.md) | [memoryRequestMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_request_min) |
| [C-0270](https://kubescape.io/docs/controls/c-0270/) | Ensure CPU limits are set | [kubescape-c-0270-deny-resources-with-cpu-limit-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0270-deny-resources-with-cpu-limit-not-set.md) | [cpuLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#cpu_limit_min) |
| [C-0271](https://kubescape.io/docs/controls/c-0271/) | Ensure memory limits are set | [kubescape-c-0271-deny-resources-with-memory-limit-not-set](/docs/policies-based-on-kubescape-controls/kubescape-c-0271-deny-resources-with-memory-limit-not-set.md) | [memoryLimitMin](https://kubescape.io/docs/frameworks-and-controls/configuring-controls/#memory_limit_min) |

## Testing Policies

### Cluster
You need a cluster that supports Validating Admission Policies. You can start a simple minikube with the script `scripts/setup-test-minikube-cluster.sh`

### Testing a single policy

You can run the tests associated with a single policy by following these steps.

```bash
cd controls/C-0016
python ../../scripts/run-control-tests.py
```

This script reads the `tests.json` file in the directory, builds the policy bindings and test objects and tests the policy with the binding against the test object.

The `tests.json` contains test cases where each case has a
* template object: a YAML in the [test-resources](/test-resources/) directory
* field changes: what changes to be done to the template object before applying it
* expected field: what should happen when applying the object after the field changes

### Learning about Validating Admission Policies

Check [this out](docs/validating-admission-policies/README.md)
