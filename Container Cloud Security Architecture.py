from diagrams import Cluster, Diagram
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.generic.database import SQL
from diagrams.generic.device import Mobile
from diagrams.generic.os import Ubuntu
from diagrams.generic.place import Datacenter

with Diagram("Container Cloud Security Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        master = Pod("Master Node")
        workers = [Pod("Worker Node 1"), Pod("Worker Node 2")]
        master - workers

    with Cluster("Security Scanning"):
        clair = SQL("Clair")
        anchore = SQL("Anchore Engine")
        for worker in workers:
            worker >> clair
            worker >> anchore

    with Cluster("Runtime Security"):
        twistlock = SQL("Twistlock")
        for worker in workers:
            worker >> twistlock

    prometheus = Prometheus("Prometheus")
    grafana = Grafana("Grafana")
    master >> prometheus >> grafana

    user = Mobile("Administrator")
    user >> grafana
    user >> twistlock

    # Additional elements for more detail
    with Cluster("Containerized Applications"):
        apps = [Pod("App 1"), Pod("App 2")]
        for worker in workers:
            for app in apps:
                worker >> app

    with Cluster("Data Storage"):
        db = SQL("Database")
        for app in apps:
            app >> db

    with Cluster("External Services"):
        ext_service = Service("External API")
        for app in apps:
            app >> ext_service

    with Cluster("Logging and Analysis"):
        logging = SQL("Logging Service")
        for app in apps:
            app >> logging
        logging >> grafana

    ubuntu = Ubuntu("Ubuntu Server")
    datacenter = Datacenter("Datacenter")
    ubuntu >> datacenter
    for worker in workers:
        worker >> ubuntu
    db >> datacenter

