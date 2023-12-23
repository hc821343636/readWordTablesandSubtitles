from diagrams import Cluster, Diagram
from diagrams.programming.framework import Spring
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.generic.database import SQL
from diagrams.onprem.vcs import Github
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.storage import PVC

with Diagram("Project Overview Mind Map", show=False, direction="TB"):
    project = Spring("Container Security Project")

    with Cluster("Features", direction="LR"):
        features = [
            Pod("Container Orchestration"),
            PVC("Asset Management"),
            Service("Vulnerability Scanning"),
            SQL("Runtime Security"),  # 用 SQL 替代 Clair
            Pod("Compliance Auditing")
        ]
        for feature in features:
            project - feature

    with Cluster("Tools & Technologies", direction="LR"):
        tools = [
            Docker("Docker"),
            Prometheus("Prometheus"),
            Grafana("Grafana"),
            Github("GitHub")
        ]
        for tool in tools:
            project - tool

    with Cluster("Users & Stakeholders", direction="LR"):
        users = [
            Users("Administrators"),
            Users("Developers"),
            Users("Security Team")
        ]
        for user in users:
            project - user

