# bigdatatools
This repo contains a Docker environment to get started with some big data tools. Watch out: The complete environment is about 25GB in size.

## Getting started
To download the environment:

    git clone https://github.com/SG87/bigdatatools.git

Afterwards you can build the environment either explicitly at the creation:
    
    cd bigdatatools
    docker-compose build

or implicitly by starting the services:
    
    cd bigdatatools
    docker-compose up
    
Watch out, the above command will build and run ALL services. If you only wish to use one or a few components, it is better to only build or start these components:
   - For one component:
    
    docker-compose up <component>
   
   - For more than one component:
   
    docker-compose up <component1> <component2> ...

To stop the environment:
    
    docker-compose down

Again, to stop one component:
    
    docker-compose down <component>

## Included components
### Portainer
[Portainer](https://www.portainer.io/) is an tool to build, manage and visualize Docker containers. It will give you a nice overview of the created and running containers, images, networks, ... Additionally, Portainer has the ability to easily monitor your environment and containers. The tool also allows to access a container via a command line tool in the browse (*docker exec -it <container_id> /bin/bash*).

Portainer is started automatically in the background with the start of every other container described below. To start Portainer explicitly, execute the following command in the *bigdatatools* directory:

    docker-compose up portainer
    
The UI of Portainer is located at *IP*:9000

You can login with the user *admin* and password *bigdatatools*

### HDFS
To have a critical setup of HDFS, you need at least a namenode and a datanode. Other components like the fileserver, secondary namenode, ... are not included in the experimental environment.

To start HDFS:
    
    docker-compose up datanode
    
With starting the datanode, the namenode (and Portainer) will automatically spin up as well.

#### Namenode
The namenode is the master of the HDFS cluster. You can start it explicitly using:
    
    docker-compose up namenode

Nevertheless it is suggested to always start the entire HDFS cluster by starting the datanode.

The interface of HDFS (namenode) runs at *IP*:50070

#### Datanode
The datanode is the worker of the HDFS cluster. This is where the data is stored and treated.

You can find the interface of the HDFS datanode at *IP*:50075

### Hue
[Hue](http://gethue.com/) is an interface on top of Hadoop. It will allow you to easily browse files, manage, create and delete file in HDFS. In more elaborate versions, it also allows you to query HDFS (using Hive), work with HBase, etc.
As this environment only contains an HDFS and no Hive or HBase, functionality is limited.

To start Hue:
    
    docker-compose up hue

HDFS (and Portainer) will be started in the background. The Hue interface will run on *IP*:8088. Notice that after login it is possible that you receive an error page. It is recommended to browse directly to *IP*:8088/home

### Spark:
[Spark](https://spark.apache.org/) is marketing itself as a *Lightning-fast unified analytics engine* and allows to perform ETL, machine learning in batch an as streams. 

Spark is a distributed tool and therefore a *master* and *worker* can be distinguished. To start the spark cluster (with one master and one worker):

    docker-compose up spark-worker

#### Master
The Spark Master can be started using:
    
    docker-compose up spark-master

Although starting the master separately is perfectly possible, it is recommended to always start it together with the worker as shown above.

The UI of Spark is located at *IP*:4040. Remark that this endpoint will only be available if Spark is started.

#### Worker
See above


### Notebooks:
Notebooks are tools that allow you to easily explore and work with data using analytics tools in your browser. In this environment Zeppelin and Jupyter are included.

Notice that both notebooks run today in stand-alone mode.

#### Jupyter
[Jupyter](https://jupyter.org/) is a highly visible notebook that allows you to work in Python, R and its Spark counterparts (PySpark and SparkR). In this environment is focused on working with PySpark. By start Jupyter notebook, using the command below, A Jupyter environment running PySpark is started.
    
    docker-compose up jupyter

When Jupyter is started, you will find the UI at *IP*:8888. Notice that you will have to enter a password which is *bigdatatools*.

Jupyter also includes a python interface to three deep learning frameworks: 

- [Tensorflow](https://www.tensorflow.org/)
- [Pytorch](https://pytorch.org/)
- [Keras](https://keras.io/)

#### Zeppelin
[Zeppelin](https://zeppelin.apache.org/) is another notebook environment which is, in my opionion, less visual, but has more strength compared to Jupyter. If you only want to work in Python, R, PySpark, or SparkR, Jupyter might be a good fit.
In contrast, Zeppelin is able connect to much more environments. Spark (with Scala), Hive (SQL), Elasticsearch and SQOOP are a few. [The entire overview](https://zeppelin.apache.org/supported_interpreters.html)

Once Zeppelin is started using the command below, it will run at *IP*:8080

    docker-compose up zeppelin

### ElasticSearch:
#### ElasticSearch
[ElasticSearch](https://www.elastic.co/products/elasticsearch) is a distributed search index that allow you to easily query data. In this environment ElasticSearch can be started using:
    
    docker-compose up elasticsearch

Elasticsearch runs at *IP*:9200.

#### Kibana
When starting Elasticsearch, a [Kibana](https://www.elastic.co/products/kibana) node, a highly visual tool that allows you to query and visualized data in ElasticSearch, will be started as well.

Kibana will run at *IP*:5601.

### Kafka:
#### Kafka
[Kafka](https://kafka.apache.org/) is a distributed streaming platform that allows you transfer high volumes of events from one place to another. You can start Kafka using:

    docker-compose up kafka

When started, Kafka will be accessible using *IP*:9092. Notice that Kafka itself has no UI. If you want to work in Kafka (with command line), you can access the container using Portainer at *IP*:9000.

#### Zookeeper
[Zookeeper](/zookeeper.apache.org) is a distributed orchestrator supporting Kafka. To be able to run Kafka, you need to run Zookeeper. If Kafka is started, Zookeeper is also automatically started. If you want to start Zookeeper explicitly without Kafka, this is possible as well:

    docker-compose up zookeeper

Zookeeper will run at *IP*:2181. Notice that like Kafka, Zookeeper has no UI, but it can be accessed using Portainer.

## Possible future extensions
- Jupyter and Zeppelin are now running stand-alone mode. It would be nice to include them in the HDFS-Spark cluster.
- Include other tools. Candidates:
    - [Hive](https://hive.apache.org/)
    - [HBase](https://hbase.apache.org/)
    - [Cassandra](https://cassandra.apache.org/)
    - [PostgreSQL](https://www.postgresql.org/)
    - [Storm](apache)
    - [Nifi](https://nifi.apache.org/)
    - [Kafka Streams](https://kafka.apache.org/documentation/streams/)
    - [Kafka connect](https://kafka.apache.org/documentation/#connectapi)
    - Kafka UI
    - [Airflow](https://airflow.apache.org/)
    - ...

## Maintainer
[Stijn Geuens](mailto:stijn.geuens@gmail.com)


