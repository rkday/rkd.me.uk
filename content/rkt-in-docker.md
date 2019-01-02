Title: Forget Docker-in-Docker, try rkt-in-Docker
Date: 2018-06-03 18:10:00
Category: Containers
Tags: docker, rkt
Slug: rkt-in-docker
Author: Rob Day

Docker is an incredibly convenient way to package, ship and run software without worrying about dependencies or compatibility, and it's therefore becoming more and more popular. But as its popularity grows, there's more and more need to run nested containers. For example:

- a build system might run in a container, to ease management of build-time dependencies, but that build system might need to build containers
- even if a build system running in a container doesn't need to build containers, it might want to run tools packaged as containers - for example, code generators
- a test framework, containerised to ease deployment, might need to spin up containers to test them

The conventional way to do this is Docker-in-Docker - either running a full Docker daemon inside a container, or exposing the host Docker socket to the container. 
