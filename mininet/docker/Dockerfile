FROM ubuntu:20.04

# ADD dashc /root/dashc
# ADD topology.py /root/.

USER root
WORKDIR /root

COPY ENTRYPOINT.sh /
COPY requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    iproute2 \
    iputils-ping \
    mininet \
    net-tools \
    openvswitch-switch \
    tcpdump \
    vim \
    x11-xserver-utils \
    openssh-server \
    xauth \
    wget \
    xterm \
    ffmpeg \
    libc6-i386 \
    bridge-utils \
    python3.8 \
    python3 \
    python3-pip \
 && rm -rf /var/lib/apt/lists/* \
 && echo AddressFamily inet >> /etc/ssh/sshd_config \
 && sed -i 's/prohibit-password/yes/' /etc/ssh/sshd_config \
 && chmod +x /ENTRYPOINT.sh \
 && /etc/init.d/ssh restart

RUN pip3 install -r /requirements.txt

EXPOSE 6633 6653 6640

ENTRYPOINT ["/ENTRYPOINT.sh"]
