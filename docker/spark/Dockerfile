# Base oficial de Apache Spark
FROM apache/spark:3.5.0

USER root

# Instalamos curl porque la imagen oficial es "slim"
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Variables de versión
ENV ICEBERG_VERSION=1.5.2

# Descarga de JARs en la ruta de Apache (/opt/spark/jars)
WORKDIR /opt/spark/jars
RUN curl -LO https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12-${ICEBERG_VERSION}.jar && \
    curl -LO https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

# Instalamos las librerías de Python
RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    pyiceberg[s3fs]==0.7.1 \
    pyarrow==15.0.1 \
    kafka-python==2.0.2 \
    requests==2.31.0 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    structlog==24.1.0

# Copiamos el conf. Nota: El origen depende de desde dónde lances el build
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

# Usuario estándar de Apache Spark
USER 185