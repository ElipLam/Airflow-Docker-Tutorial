# Airflow-Docker-Tutorial
My self-learning about Airflow with Docker.

## Table of Contents
- [Docker](#docker)
  - [Install Docker](#install-docker)
    - [Ubuntu](#ubuntu)
    - [Fedora](#fedora)
  - [Install docker-compose](#install-docker-compose)
  - [Start docker](#start-docker)
  - [Verify that Docker Engine](#verify-that-docker-engine)
  - [Run image with bash shell](#run-image-with-bash-shell)
  - [Executing the Docker Command Without Sudo](#executing-the-docker-command-without-sudo)
  - [Fixed: NoPermissions (FileSystemError): Error: EACCES: permission denied.](#fixed-nopermissions-filesystemerror-error-eacces-permission-denied)
  - [Uninstall docker–compose](#uninstall-dockercompose)
  - [Uninstall Docker Engine](#uninstall-docker-engine)
- [Airflow with Docker](#airflow-with-docker)
  - [Install Airflow](#install-airflow)
  - [Create airflow_docker_sample folder](#create-airflow_docker_sample-folder)
  - [Initializing Environment](#initializing-environment)
  - [Run Airflow](#run-airflow)
  - [Accessing the web interface](#accessing-the-web-interface)
  - [Add user for airflow](#add-user-for-airflow)
  - [Extending Airflow Image](#extending-airflow-image)
- [Refer](#refer)

# Docker

## Install Docker 

### [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) 
### [Fedora](https://docs.docker.com/engine/install/fedora/) 

## Install docker-compose
```console
sudo apt-get update
sudo apt-get upgrade

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
sudo docker–compose --version
```

## Start docker 
```console
sudo systemctl start docker
```

## Verify that Docker Engine 

Verify that Docker Engine is installed correctly by running the hello-world image

```console
sudo docker run hello-world
```

## Run image with bash shell
```console
docker-compose up -d
# docker run -it --name myimage
docker run -it --name apache/airflow
```
## Executing the Docker Command Without Sudo

By default, the `docker` command can only be run the **root** user or by a user in the **docker** group, which is automatically created during Docker’s installation process. If you attempt to run the `docker` command without prefixing it with `sudo` or without being in the **docker** group, you’ll get an output like this:

```console
Output:
docker: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
See 'docker run --help'.
```

If you want to avoid typing `sudo` whenever you run the `docker` command, add your username to the `docker` group:

```console
sudo usermod -aG docker ${USER}
```

To apply the new group membership, log out of the server and back in, or type the following:

```console
su - ${USER}
```

You will be prompted to enter your user’s password to continue.

Confirm that your user is now added to the docker group by typing:

```console
groups
```


```console
Output:
sammy sudo docker
```

If you need to add a user to the **docker** group that you’re not logged in as, declare that username explicitly using:


```console
sudo usermod -aG docker username
```
The rest of this article assumes you are running the `docker` command as a user in the **docker** group. If you choose not to, please prepend the commands with `sudo`.

Let’s explore the `docker` command next.


## Fixed: NoPermissions (FileSystemError): Error: EACCES: permission denied.

```console
# sudo chown -R <user-name> <directory-name>
sudo chown -R ubuntu /home/ubuntu
sudo chown -R ubuntu /usr/bin/docker-compose

docker exec -u root -ti my_airflow_container_id bash 

# In this case it's the scheduler container - after this you cd out to the outer base dir
# Then do 
chmod -R 777 /opt
chown 50000:50000 dags logs plugins
sudo chmod u=rwx,g=rwx,o=rwx /home/ubuntu/airflow_logs
```


## Uninstall docker–compose

Debian/Ubuntu:
```console
sudo rm /usr/bin/docker-compose
sudo apt remove docker-compose
#sudo apt autoremove
```

## Uninstall Docker Engine

Docker Community Edition (CE) 

Fedora:
```console
sudo dnf remove docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Images, containers, volumes, or customized configuration files on your host are not automatically removed. To delete all images, containers, and volumes

```console
 sudo rm -rf /var/lib/docker
 sudo rm -rf /var/lib/containerd
```

# Airflow with Docker

## Install Airflow

You should at least allocate 4GB memory for the Docker Engine (ideally 8GB). You can check and change the amount of memory in [Resources](https://docs.docker.com/desktop/get-started/).

You can also check if you have enough memory by running this command:

```console
docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
```

## Create airflow_docker_sample folder

```console
mkdir airflow_docker_sample
cd airflow_docker_sample
```

To deploy Airflow on Docker Compose, you should fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml).

```console
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'
```

or

use [my custom docker-compose.yaml](./docker-compose.yaml).

## Initializing Environment

Before starting Airflow for the first time, You need to prepare your environment, i.e. create the necessary files, directories and initialize the database.

Setting the right Airflow user.

```console
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

```console
AIRFLOW_UID=50000
```

## Run Airflow

```console
docker-compose up -d
```

## Accessing the web interface

Once the cluster has started up, you can log in to the web interface and try to run some tasks.

The webserver is available at: `http://localhost:8080`. The default account has the login `airflow` and the password `airflow`.

## Add user for airflow

Add user account in case Airflow runs but no Admin.

```console
airflow users  create --role Admin --username airflow --email admin --firstname elip --lastname lam --password airflow
```

`PATH=$PATH:~/.local/bin`

## Extending Airflow Image

My image includes the following libraries: 
- numpy
- requests
- pandas
- progress
- boto3
- pyspark
- awswrangler

See *Dockerfile* and *Dockerfile_update* to know more details.

**Build docker file**

Syntax: *docker build . -f Dockerfile --pull --tag my-image:0.0.1*

```console
docker build . -f Dockerfile --tag eliplam/airflow_pyspark:0.0.1
```

Here is [my image](https://hub.docker.com/repository/docker/eliplam/airflow_pyspark) in Docker hub.

# Refer

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 

https://airflow.apache.org/docs/docker-stack/build.html

https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

https://docs.docker.com/develop/develop-images/multistage-build/

###### [on top](#table-of-contents)