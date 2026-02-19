FROM apache/spark:3.5.0
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
ENV ICEBERG_VERSION=1.5.2
WORKDIR /opt/spark/jars
RUN curl -LO https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar &&     curl -LO https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar
RUN pip install --no-cache-dir pyspark==3.5.0 pyiceberg[s3fs]==0.7.1 pyarrow==15.0.1 kafka-python==2.0.2 requests==2.31.0 pydantic==2.5.0 pydantic-settings==2.1.0 structlog==24.1.0
ENV SPARK_VERSION=3.5.0
ENV SCALA_VERSION=2.12
RUN curl -L -o /opt/spark/jars/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar "https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar" \
 && curl -L -o /opt/spark/jars/kafka-clients-3.6.1.jar "https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.6.1/kafka-clients-3.6.1.jar" \
 && curl -L -o /opt/spark/jars/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar "https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar" \
 && curl -L -o /opt/spark/jars/commons-pool2-2.12.0.jar "https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar"
USER 185
