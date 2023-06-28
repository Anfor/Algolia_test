FROM apache/airflow:2.2.0

USER root

ENV DEBIAN_FRONTEND=noninteractive \
    TERM=linux \
    AIRFLOW_GPL_UNIDECODE=yes

RUN apt-get -y update \
 && apt-get -y install python-pip libpq-dev postgresql-client python3-dev python3-distutils python3-apt openjdk-11-jdk



# Set Java home environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Download and install Spark
ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=3
RUN curl -O https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set Spark home environment variable
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

USER airflow

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir psycopg2 pytest findspark moto
