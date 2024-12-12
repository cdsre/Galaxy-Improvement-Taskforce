# Configuring OTEL

We will use the opentelemetry operator and install it via helm with a self-signed certificate.

```shell
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm install my-opentelemetry-operator open-telemetry/opentelemetry-operator \
  --set "manager.collectorImage.repository=otel/opentelemetry-collector-k8s" \
  --set admissionWebhooks.certManager.enabled=false \
  --set admissionWebhooks.autoGenerateCert.enabled=true
```

Once installed you can read more about configuring auto-instrumentation in the docs 
https://opentelemetry.io/docs/kubernetes/operator/automatic/#did-the-instrumentation-resource-install