# gke-opentelemetry-setup

## Steps to setup tracing with OpenTelemetry

* Enable Cloud Trace API in GCP
* Cluster service account needs `roles/cloudtrace.agent` role or create new service account
* Install OpenTelemetry operator: 
```bash
kubectl apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/download/v0.60.0/opentelemetry-operator.yaml
```
* Deploy Collector, there are options to deploy it as sidecar or as separate pod
```bash
kubectl apply -f collector-config.yaml
```
* As an option we can also install auto-instrumentator and we do not have to make changes to code but customization is limited. To make it work we have to annotate our pods with `k apply -f collector-config.yaml`
![Trace](docs/log_2.png)
* [Docs to check how we can setup traces](https://google-cloud-opentelemetry.readthedocs.io/en/latest/index.html)


* Check repository for additional [Opentelemetry instrumentation](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation) options for example: 
 - `celery`
 - `django`
 - `aiohttp`
 - `sqlalchemy`

This instrumentators can enhance our tracing for specific libraries.
## Logging

We can also improve our logging with google sdk. We can add additional data in a structured way.

* https://cloud.google.com/logging/docs/reference/libraries#logging_write_log_entry_advanced-go
* https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#httprequest/

![Logs](docs/log_1.png)