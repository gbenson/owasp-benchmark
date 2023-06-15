# docker build --tag gbenson/owasp-benchmark:latest --file VMs/Dockerfile .
FROM ubuntu:jammy

RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -q -y \
     openjdk-8-jre-headless \
     openjdk-8-jdk \
     git \
     maven \
     wget \
     iputils-ping \
     && apt-get clean

RUN mkdir /owasp
WORKDIR /owasp

# Download, build, install Benchmark Utilities required by crawler and scorecard generation
RUN git clone https://github.com/gbenson/owasp-benchmark-utils.git BenchmarkUtils
WORKDIR /owasp/BenchmarkUtils
RUN mvn install

# Incorporate current checkout as /owasp/BenchmarkJava
WORKDIR /owasp
RUN mkdir /owasp/BenchmarkJava
COPY . BenchmarkJava

# Workaround for security fix for CVE-2022-24765
RUN git config --global --add safe.directory /owasp/BenchmarkJava

# Make Spotless ratchet against local checkout's main branch
RUN sed -i 's,origin/master,main,g' BenchmarkJava/pom.xml

# Build BenchmarkJava
WORKDIR /owasp/BenchmarkJava
RUN mvn clean package cargo:install

RUN useradd -d /home/bench -m -s /bin/bash bench 
RUN echo bench:bench | chpasswd

RUN chown -R bench /owasp/
ENV PATH /owasp/BenchmarkJava:$PATH

# start up Benchmark once, for 60 seconds, then kill it, so the additional dependencies required to run it are downloaded/cached in the image as well.
# exit 0 is required to return a 'success' code, otherwise the timeout returns a failure code, causing the Docker build to fail.
WORKDIR /owasp/BenchmarkJava
RUN timeout 60 ./runBenchmark.sh; exit 0

