## What is sRNAtoolbox?

[**sRNAtoolbox**](https://academic.oup.com/nar/article/50/W1/W710/6584784?login=false) is a collection of several tools for small RNA research including expression profiling from NGS data, differential expression, analysis of unmapped reads with blast and consensus target prediction and analysis.

The key tool of sRNAtoolbox is **sRNAbench** (Barturen _et al._, 2014) which is the successor program of **miRanalyzer** (Hackenberg _et al._, 2009, 2011) a tool for expression profiling of small RNAs and prediction of novel microRNAs.

sRNAtoolbox is implemented into a [webserver](https://arn.ugr.es/srnatoolbox), **a Docker**, and some of the tools are also available as [standalone executable files in this repository.](https://github.com/bioinfoUGR/sRNAtoolbox/tree/master/exec) These tools are provided under an [MIT license](./LICENSE).

## Citing sRNAtoolbox or sRNAbench
If you use sRNAbench or sRNAtoolbox please make sure to cite our latest publication.
>Aparicio-Puerta E., Gómez-Martín C., Giannoukakos S., Medina J.M., Scheepbouwer C., García-Moreno A., Carmona-Saez P., Fromm B., Pegtel D.M., Keller A., Marchal J.A.,  Hackenberg M., sRNAbench and sRNAtoolbox 2022 update: accurate miRNA and sncRNA profiling for model and non-model organisms, Nucleic Acids Research, Volume 50, Issue W1, 5 July 2022, Pages W710–W717, [https://doi.org/10.1093/nar/gkac363](https://doi.org/10.1093/nar/gkac363).

## Getting started

There are 3 ways to use sRNAbench or sRNAtoolbox: Webserver, Docker container or standalone versions. We discourage the usage of standalone as several dependencies exist. 

### Webserver
The easiest way is to use the webserver which can be accessed here: [sRNAtoolbox webserver](https://arn.ugr.es/srnatoolbox). 

### sRNAtoolbox Docker
The sRNAtoolbox docker provides the user with a concealed environment containing all sRNAtoolbox tools and their dependencies such as Vienna package, bowtie, samtools etc. needed for common small RNA data analysis. 

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
