#Selector

Concurrently and temporarily share the same clusters of resources between consumers.

[![Docker Repository on Quay](https://quay.io/repository/jcmoraisjr/selector/status "Docker Repository on Quay")](https://quay.io/repository/jcmoraisjr/selector)

#Usage

Running the service as a Docker container:

    docker run -d -p 8000:8000 quay.io/jcmoraisjr/selector \
      --clusters-inline='{"cl":["res1","res2","res3"]}'

Running the server outside Docker. Clone this repository and:

    python selector.py --clusters-inline='{"cl":["res1","res2","res3"]}'

Acquire and lock some resources:

    curl -d'{"qty":1,"cluster":"cl"}' localhost:8000/acquire

Output:

    {"status": "ok", "items": ["res1"], "id": "id1"}

Release the resource(s) back to the cluster:

    curl -id'{"id":"id1"}' localhost:8000/release

#Options

* `--clusters-inline` Provide the cluster resources inline.
* `--clusters-file` Point to a file with the cluster resources. Either inline or file should be provided.
* `--locks` Optional, where locks should be stored. Store outside the container if you want to save current locks between restarts.
* `--port` Optional, defaults to `8000`.

#Clusters configuration

Declare a single object (dict in Python) where the key is the name of the cluster and the value is an array (list in Python) of resources available.

Declaring 2 clusters of 3 resources:

    {
        "cluster1": [
            "res1_1",
            "res1_2",
            "res1_3"
        ],
        "cluster2": [
            "res2_1",
            "res2_2",
            "res2_3"
        ]
    }

#Deploy

Create a directory where Selector will save current locks:

    mkdir -p /var/lib/selector
    chown 1000:1000 /var/lib/selector

Deploy this systemd unit. Change the `--clusters-inline` info or mount and point a json file using `--clusters-file`.

    [Unit]
    Description=Selector
    After=docker.service
    Requires=docker.service
    [Service]
    ExecStartPre=-/usr/bin/docker stop selector
    ExecStartPre=-/usr/bin/docker rm selector
    ExecStart=/usr/bin/docker run \
      --name selector \
      -p 8000:8000 \
      -v /var/lib/selector:/var/lib/selector \
      quay.io/jcmoraisjr/selector:latest \
        --locks=/var/lib/selector/locks.json \
        --clusters-inline='{"cl":["res1","res2","res3"]}'
    ExecStop=-/usr/bin/docker stop selector
    RestartSec=10s
    Restart=always
    [Install]
    WantedBy=multi-user.target

#Wishlist

* Query used resources
* Define an amount of time to wait until a resource is available
* Round robin
