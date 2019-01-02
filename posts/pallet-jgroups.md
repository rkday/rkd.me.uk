---
layout: default.liquid
title: Reconfiguring an AWS Elastic IP with Pallet
published_date: 2013-12-08 21:50:00 +0100
slug: pallet-elastic-ip
---

I was recently playing around with Pallet (as an offshoot of some of the DevOps-style cloud provisioning work I do on [Project Clearwater](http://www.projectclearwater.org)), and had a bit of trouble getting from Pallet to the underlying jClouds API (I was using 1.5.5).

Specifically, I wanted to associate an EC2 elastic IP address with the new node I'd created with Pallet, effectively making it a drop-in replacement for a failed box.

This is the code I ended up with, relying on the fact that pallet.api/converge returns a map with a :environment parameter, which in turn has a :compute object which is a jClouds ComputeService object, which you can do Java interop on:

```clojure
(let [node-data (pallet.api/converge ...)
      node (:node (first (:new-nodes node-data)))
      compute (:compute (:environment node-data))]
    (-> compute
        .getContext
        .getProviderSpecificContext ; AWS-specific function
        .getApi ; [1]
        .getElasticIPAddressServices
        (.associateAddressInRegion "us-east-1", "54.204.28.146", (.getProviderId node)))) ; [2]
```

[1] .getApi returns an [AWSEC2Client](http://demobox.github.io/jclouds-maven-site-1.5.5/1.5.5/jclouds-multi/apidocs/org/jclouds/aws/ec2/AWSEC2Client.html), which you can use to access other EC2 services.

[2] Obviously, this elastic IP was specific to me (and I've since deleted it).

Since then, I've found that there is a [nicer Clojure interface to jClouds](https://github.com/jclouds/jclouds/blob/328679799b7ae7bf6eed731a528e773c8fbd5e2f/aws/core/src/main/clojure/org/jclouds/aws/elastic_ip.clj). I haven't tested it, but the above code should then look something like this:

```clojure
(let [node-data (pallet.api/converge ...)
      node (:node (first (:new-nodes node-data)))
      compute (:compute (:environment node-data))
      eip (org.jclouds.aws.elastic-ip/eip-service compute)]
      (with-compute-service [compute]
        (org.jclouds.aws.elastic-ip/associate node "54.204.28.146")))
```
