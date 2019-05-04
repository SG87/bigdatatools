FROM gettyimages/spark:2.4.0-hadoop-3.0

# SciPy

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    libpython3-dev \
    build-essential \
    pkg-config \
    gfortran \
    ca-certificates \
    wget \
    liblapack-dev \
    libopenblas-dev
RUN  pip3 install numpy pandasql scipy jupyter tensorflow faker stopwords tweepy kafka torch torchvision stopwords stop_words

# Jupyter

RUN jupyter notebook --generate-config \
 && echo "c.NotebookApp.allow_root=True" >> /root/.jupyter/jupyter_notebook_config.py \
 && echo "c.NotebookApp.token='bigdatatools'" >> /root/.jupyter/jupyter_notebook_config.py \
 && echo "c.NotebookApp.open_browser=False" >> /root/.jupyter/jupyter_notebook_config.py \
 && echo "c.NotebookApp.notebook_dir='/notebooks'" >> /root/.jupyter/jupyter_notebook_config.py

#RUN mkdir $SPARK_HOME/jars
COPY ./conf/elasticsearch-spark-20_2.11-6.5.4.jar $SPARK_HOME/jars/
COPY ./conf/spark-streaming-kafka-0-8_2.11-2.4.0.jar $SPARK_HOME/jars/
COPY ./conf/spark-sql-kafka-0-10_2.11-2.4.0.jar $SPARK_HOME/jars/

RUN echo "spark.driver.extraClassPath $SPARK_HOME/jars/elasticsearch-spark-20_2.11-6.5.4.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraClassPath $SPARK_HOME/jars/elasticsearch-spark-20_2.11-6.5.4.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.driver.extraLibraryPath $SPARK_HOME/jars/elasticsearch-spark-20_2.11-6.5.4.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraLibraryPath $SPARK_HOME/jars/elasticsearch-spark-20_2.11-6.5.4.jar" >> $SPARK_HOME/conf/spark-defaults.conf

RUN echo "spark.driver.extraClassPath $SPARK_HOME/jars/spark-streaming-kafka-0-8_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraClassPath $SPARK_HOME/jars/spark-streaming-kafka-0-8_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.driver.extraLibraryPath $SPARK_HOME/jars/spark-streaming-kafka-0-8_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraLibraryPath $SPARK_HOME/jars/spark-streaming-kafka-0-8_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf

RUN echo "spark.driver.extraClassPath $SPARK_HOME/jars/spark-sql-kafka-0-10_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraClassPath $SPARK_HOME/jars/spark-sql-kafka-0-10_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.driver.extraLibraryPath $SPARK_HOME/jars/spark-sql-kafka-0-10_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf
RUN echo "spark.executor.extraLibraryPath $SPARK_HOME/jars/spark-sql-kafka-0-10_2.11-2.4.0.jar" >> $SPARK_HOME/conf/spark-defaults.conf


ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS='notebook --no-browser --port=8888 --ip=0.0.0.0'

WORKDIR $SPARK_HOME
EXPOSE 8888 9009
CMD ["bin/pyspark"]