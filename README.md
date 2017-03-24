docker-locust
=============
Dockerfile to create [Docker](https://www.docker.io/) containers for [Locust](https://github.com/locustio/locust) load testing tool.

Build or Image
=====
You can either build your own image using the included ```Dockerfile``` or just pull the existing image from the Docker Index.

#### Build container:
```bash
$ docker build -t [user|organization]/locust .
$ docker images
$ docker tag [user|organization]/locust my-registry:5000/my-image
$ docker push my-registry:5000/my-image
$ docker rmi [user|organization]/locust
```

#### Pull image:
```bash
$ docker pull [user|organization]/locust
```

Usage
=====
The following usage instructions assumes Docker `>= 0.5.3` and your running
user in the `docker` system group (to prevent needed `sudo` usage).

#### Run in Single node mode:
```bash
$ docker run -d -e host='http://<insert_target_host>' -v `pwd`/locustfiles:/opt/locustfiles [user|organization]/locust locust -f /opt/locustfiles/locustfile.py
```

#### Run as Master:
```bash
$ docker run -d -e host='http://<insert_target_host>' -p 8089:8089 -p 5557:5557 -p 5558:5558 -v `pwd`/locustfiles:/opt/locustfiles [user|organization]/locust locust --master -f /opt/locustfiles/locustfile.py
```

#### Run as Slave:
```bash
$ docker run -d -e host='http://<insert_target_host>' -v `pwd`/locustfiles:/opt/locustfiles [user|organization]/locust locust --slave --master-host=<ip_of_docker_host> -f /opt/locustfiles/locustfile.py
```

The locustfile.py included is just an example that uses an evironment variable to load information. To use your own locustfile, just change ```-v `pwd`/locustfiles:/opt/locustfiles``` to point to your own locustfile.

Once your master/standalone container is running, connect to your Docker host on 8089 to access the webui.
