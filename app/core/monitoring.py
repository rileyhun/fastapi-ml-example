from prometheus_client import Histogram, Counter, Summary
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import os
from typing import Callable

NAMESPACE = os.environ.get("METRICS_NAMESPACE", "fastapi")
SUBSYSTEM = os.environ.get("METRICS_SUBSYSTEM", "model")

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)

# ----- custom metrics -----
def classification_model_confidence(
    metric_name: str = "classification_model_confidence",
    metric_doc: str = "confidence score of classification model",
    metric_namespace: str = "",
    metric_subsystem: str = "",
    buckets=(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1)
) -> Callable[[Info], None]:

    METRIC = Histogram(
        metric_name,
        metric_doc,
        buckets=buckets,
        namespace=metric_namespace,
        subsystem=metric_subsystem
    )

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/predict":
            model_prob = info.response.headers.get("X-model-proba")
            if model_prob:
                METRIC.observe(float(model_prob))

    return instrumentation

def classification_model_label(
    metric_name: str = "classification_model_label",
    metric_doc: str = "model predictions of classification model",
    metric_namespace: str = "",
    metric_subsystem: str = ""
) -> Callable[[Info], None]:
    METRIC = Counter(
        metric_name,
        metric_doc,
        namespace=metric_namespace,
        subsystem=metric_subsystem,
        labelnames=('labels',)
    )
    def instrumentation(info: Info) -> None:
        if info.modified_handler == '/predict':
            METRIC.labels(info.response.headers.get('X-model-predict')).inc()

    return instrumentation

# ----- add metrics -----
instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)

instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)

instrumentator.add(
    classification_model_label(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM)
)

instrumentator.add(
    classification_model_confidence(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM)
)

