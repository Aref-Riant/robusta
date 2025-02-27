import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from urllib.parse import unquote_plus, urlparse

from hikaru.model import DaemonSet, Node, StatefulSet
from pydantic import BaseModel

from robusta.core.reporting import Finding, FindingSeverity, FindingSource, FindingSubject, FindingSubjectType
from robusta.integrations.kubernetes.autogenerated.events import (
    DaemonSetEvent,
    DeploymentEvent,
    JobEvent,
    NodeEvent,
    PodEvent,
    StatefulSetEvent,
)
from robusta.integrations.kubernetes.custom_models import RobustaDeployment, RobustaJob, RobustaPod

SEVERITY_MAP = {
    "critical": FindingSeverity.HIGH,
    "error": FindingSeverity.MEDIUM,
    "warning": FindingSeverity.LOW,
    "info": FindingSeverity.INFO,
}


# for parsing incoming data
class PrometheusAlert(BaseModel):
    endsAt: datetime
    generatorURL: str
    startsAt: datetime
    fingerprint: Optional[str] = ""
    status: str
    labels: Dict[Any, Any]
    annotations: Dict[Any, Any]


# for parsing incoming data
class AlertManagerEvent(BaseModel):
    alerts: List[PrometheusAlert] = []
    externalURL: str
    groupKey: str
    version: str
    commonAnnotations: Optional[Dict[Any, Any]] = None
    commonLabels: Optional[Dict[Any, Any]] = None
    groupLabels: Optional[Dict[Any, Any]] = None
    receiver: str
    status: str


# everything here needs to be optional due to annoying subtleties regarding dataclass inheritance
# see explanation in the code for BaseEvent
@dataclass
class PrometheusKubernetesAlert(PodEvent, NodeEvent, DeploymentEvent, JobEvent, DaemonSetEvent, StatefulSetEvent):
    alert: Optional[PrometheusAlert] = None
    alert_name: Optional[str] = None
    alert_severity: Optional[str] = None
    label_namespace: Optional[str] = None
    node: Optional[Node] = None
    pod: Optional[RobustaPod] = None
    deployment: Optional[RobustaDeployment] = None
    job: Optional[RobustaJob] = None
    daemonset: Optional[DaemonSet] = None
    statefulset: Optional[StatefulSet] = None

    def get_node(self) -> Optional[Node]:
        return self.node

    def get_pod(self) -> Optional[RobustaPod]:
        return self.pod

    def get_deployment(self) -> Optional[RobustaDeployment]:
        return self.deployment

    def get_job(self) -> Optional[RobustaJob]:
        return self.job

    def get_daemonset(self) -> Optional[DaemonSet]:
        return self.daemonset

    def get_title(self) -> str:
        annotations = self.alert.annotations
        if annotations.get("summary"):
            return f'{annotations["summary"]}'
        else:
            return self.alert.labels.get("alertname", "")

    def get_prometheus_query(self) -> str:
        """
        Gets the prometheus query that defines this alert.
        """
        url = urlparse(self.alert.generatorURL)
        return re.match(r"g0.expr=(.*)&g0.tab=1", unquote_plus(url.query)).group(1)

    def get_description(self) -> str:
        annotations = self.alert.annotations
        clean_description = ""
        if annotations.get("description"):
            # remove "LABELS = map[...]" from the description as we already add a TableBlock with labels
            clean_description = re.sub(r"LABELS = map\[.*\]$", "", annotations["description"])
        return clean_description

    def get_alert_subject(self) -> FindingSubject:
        subject_type: FindingSubjectType = FindingSubjectType.TYPE_NONE
        name: Optional[str] = "Unresolved"
        namespace: Optional[str] = self.label_namespace
        node_name: Optional[str] = None
        if self.deployment:
            subject_type = FindingSubjectType.TYPE_DEPLOYMENT
            name = self.deployment.metadata.name
            namespace = self.deployment.metadata.namespace
        elif self.daemonset:
            subject_type = FindingSubjectType.TYPE_DAEMONSET
            name = self.daemonset.metadata.name
            namespace = self.daemonset.metadata.namespace
        elif self.statefulset:
            subject_type = FindingSubjectType.TYPE_STATEFULSET
            name = self.statefulset.metadata.name
            namespace = self.statefulset.metadata.namespace
        elif self.node:
            subject_type = FindingSubjectType.TYPE_NODE
            name = self.node.metadata.name
            node_name = self.node.metadata.name
        elif self.pod:
            subject_type = FindingSubjectType.TYPE_POD
            name = self.pod.metadata.name
            namespace = self.pod.metadata.namespace
            node_name = self.pod.spec.nodeName
        elif self.job:
            subject_type = FindingSubjectType.TYPE_JOB
            name = self.job.metadata.name
            namespace = self.job.metadata.namespace

        return FindingSubject(name, subject_type, namespace, node_name)

    def create_default_finding(self) -> Finding:
        alert_subject = self.get_alert_subject()
        status_message = "[RESOLVED] " if self.alert.status.lower() == "resolved" else ""
        title = f"{status_message}{self.get_title()}"
        # AlertManager sends 0001-01-01T00:00:00Z when there's no end date
        ends_at = self.alert.endsAt if self.alert.endsAt.timestamp() > 0 else None
        return Finding(
            title=title,
            description=self.get_description(),
            source=FindingSource.PROMETHEUS,
            aggregation_key=self.alert_name,
            severity=SEVERITY_MAP.get(self.alert.labels.get("severity"), FindingSeverity.INFO),
            subject=alert_subject,
            fingerprint=self.alert.fingerprint,
            starts_at=self.alert.startsAt,
            ends_at=ends_at,
            add_silence_url=True,
            silence_labels=self.alert.labels,
        )

    def get_subject(self) -> FindingSubject:
        return self.get_alert_subject()

    @classmethod
    def get_source(cls) -> FindingSource:
        return FindingSource.PROMETHEUS

    def get_resource(self) -> Optional[Union[RobustaPod, DaemonSet, RobustaDeployment, StatefulSet, Node, RobustaJob]]:
        kind = self.get_subject().subject_type
        if kind == FindingSubjectType.TYPE_DEPLOYMENT:
            return self.deployment
        elif kind == FindingSubjectType.TYPE_DAEMONSET:
            return self.daemonset
        elif kind == FindingSubjectType.TYPE_STATEFULSET:
            return self.statefulset
        elif kind == FindingSubjectType.TYPE_NODE:
            return self.node
        elif kind == FindingSubjectType.TYPE_POD:
            return self.pod
        elif kind == FindingSubjectType.TYPE_JOB:
            return self.job
        return None
