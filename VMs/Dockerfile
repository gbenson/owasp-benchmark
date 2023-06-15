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

# Incorporate and build current checkout as /owasp/BenchmarkJava
WORKDIR /owasp
RUN mkdir /owasp/BenchmarkJava
WORKDIR /owasp/BenchmarkJava
COPY . .
RUN python3 VMs/disable-spotless.py
RUN mvn clean package cargo:install

RUN useradd -d /home/bench -m -s /bin/bash bench 
RUN echo bench:bench | chpasswd

RUN chown -R bench /owasp/
ENV PATH /owasp/BenchmarkJava:$PATH

# start up Benchmark once, for 60 seconds, then kill it, so the additional dependencies required to run it are downloaded/cached in the image as well.
# exit 0 is required to return a 'success' code, otherwise the timeout returns a failure code, causing the Docker build to fail.
WORKDIR /owasp/BenchmarkJava
RUN timeout 60 ./runBenchmark.sh; exit 0

# Set up to run like this:
# docker run --rm -it -p 8443:8443 gbenson/owasp-benchmark
EXPOSE 8443
CMD ["./runRemoteAccessibleBenchmark.sh"]
