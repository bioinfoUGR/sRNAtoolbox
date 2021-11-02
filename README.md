## What is sRNAtoolbox?

[**sRNAtoolbox**](http://nar.oxfordjournals.org/content/early/2015/05/26/nar.gkv555.long) is a collection of several tools for RNA based research, including expression profiling from NGS data, differential expression, analysis of unmapped reads with blast and consensus target prediction and analysis.

The key tool of sRNAtoolbox is **sRNAbench** (Barturen _et al._, 2014) which is the successor program of **miRanalyzer** (Hackenberg _et al._, 2009, 2011) a tool for expression profiling of small RNAs and prediction of novel microRNAs.

sRNAtoolbox is implemented into a [webserver](https://arn.ugr.es/srnatoolbox), **a Docker**, and some of the programs can be furthermore downloaded as [standalone](https://bioinfo2.ugr.es/srnatoolbox/standalone/) versions.

## Getting started

There are 3 ways to use sRNAtoolbox (or parts of it): Webserver, Docker (VM) or standalone versions. We discourage the usage of standalone as several dependencies exist. 

### Webserver
The easiest way is to use the webserver which can be accessed here: [sRNAtoolbox webserver](https://arn.ugr.es/srnatoolbox). 

### sRNAtoolbox Docker
The sRNAtoolbox docker provides the user with a number of preinstalled programs like all sRNAtoolbox tools, Vienna package, bowtie, samtools etc. needed for common small RNA data analysis. 

First of all Docker must be installed. To install Docker in Ubuntu and MacOS please do the following: 

1- Install docker
```
sudo apt update
sudo apt install docker.io
```

2- Start docker as a service
```
	sudo systemctl start docker
	sudo systemctl enable docker
```
To install Docker Desktop in Windows please follow [these](https://docs.docker.com/docker-for-windows/install/) instructions.

sRNAtoolbox docker is hosted in Dockerhub so the first step is to pull the image from it:

```
sudo docker pull ugrbioinfo/srnatoolbox:latest
```
You can also download the latest image from this github, and then load it as it follows:

```
sudo docker load -i ugrbioinfo_latest.tar.gz
```

After this, your sRNAtoolbox docker image is downloaded and now you can launch it:
```
sudo docker run --hostname sRNAtoolbox --name sRNAtoolbox --user srna --workdir /home/srna -it ugrbioinfo/srnatoolbox:latest /bin/bash
```

Alternatively if you want to start the container with shared folders:

```
sudo docker run --hostname sRNAtoolbox --name sRNAtoolbox --user srna --workdir /home/srna --mount type=bind,source=MACHINE_FOLDER,destination=/shared/shared_folder -it ugrbioinfo/srnatoolbox:latest /bin/bash
```

After the first use you can exit the container by typing “exit” and stop the container with the following:
```
sudo docker stop sRNAtoolbox
```

For further uses:
```
sudo docker start sRNAtoolbox 
sudo docker exec -term=SCREEN -it sRNAtoolbox /bin/bash
```
