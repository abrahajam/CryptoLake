# ============================================================
# CryptoLake — Spark + Iceberg Docker Image
# ============================================================
# Base: apache/spark:3.5.0 (Debian, JDK 17, user 185)
#
# CLASSPATH FIX: The apache/spark entrypoint builds the JVM
# classpath from $SPARK_CLASSPATH BEFORE Spark initialises its
# catalog plugin classes.  Without this env-var, JARs sitting
# in /opt/spark/jars/ are NOT guaranteed to be on the driver
# classpath during the critical early-init phase, which causes:
#
#   ClassNotFoundException: org.apache.iceberg.spark.SparkCatalog
#
# Setting SPARK_CLASSPATH=/opt/spark/jars/* solves it.
# ============================================================

FROM apache/spark:3.5.0
USER root

# ── System deps ───────────────────────────────────────────
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# ── Version pins ──────────────────────────────────────────
ENV ICEBERG_VERSION=1.5.2
ENV SPARK_VERSION=3.5.0
ENV SCALA_VERSION=2.12

# ── Download Iceberg JARs ─────────────────────────────────
# NOTE: The Maven Central path MUST include the version directory
# segment, e.g. …/iceberg-spark-runtime-3.5_2.12/1.5.2/…
# Without it, curl downloads an HTML 404 page instead of a JAR.
WORKDIR /opt/spark/jars

RUN curl -L -o iceberg-spark-runtime-3.5_${SCALA_VERSION}-${ICEBERG_VERSION}.jar \
      "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_${SCALA_VERSION}/${ICEBERG_VERSION}/iceberg-spark-runtime-3.5_${SCALA_VERSION}-${ICEBERG_VERSION}.jar" && \
    curl -L -o iceberg-aws-bundle-${ICEBERG_VERSION}.jar \
      "https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar"

# ── Download Kafka JARs (Structured Streaming) ───────────
RUN curl -L -o spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar \
      "https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-sql-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar" && \
    curl -L -o kafka-clients-3.6.1.jar \
      "https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.6.1/kafka-clients-3.6.1.jar" && \
    curl -L -o spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar \
      "https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_${SCALA_VERSION}/${SPARK_VERSION}/spark-token-provider-kafka-0-10_${SCALA_VERSION}-${SPARK_VERSION}.jar" && \
    curl -L -o commons-pool2-2.12.0.jar \
      "https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar"

# ── Ensure all JARs are readable by user 185 (WSL2 fix) ──
RUN chmod -R a+r /opt/spark/jars/

# ── Python dependencies ──────────────────────────────────
RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    pyiceberg[s3fs]==0.7.1 \
    pyarrow==15.0.1 \
    kafka-python==2.0.2 \
    requests==2.31.0 \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0 \
    structlog==24.1.0

# ── Spark configuration ──────────────────────────────────
COPY spark-defaults.conf /opt/spark/conf/spark-defaults.conf

# ── KEY FIX: Inject JARs into JVM classpath at boot time ─
# The entrypoint of apache/spark reads SPARK_CLASSPATH and
# appends it to the JVM -cp flag BEFORE Spark initialises
# its catalog plugins.  This is what makes Iceberg classes
# visible to the classloader.
ENV SPARK_CLASSPATH="/opt/spark/jars/*"

# ── Non-root Spark user ──────────────────────────────────
USER 185
