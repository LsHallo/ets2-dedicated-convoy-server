FROM steamcmd/steamcmd:ubuntu

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN steamcmd +force_install_dir /app +login anonymous +app_update 1948160 +quit

RUN apt-get update && apt-get install -y nano python3 \
    && mkdir -p "/root/.local/share/Euro Truck Simulator 2"

COPY ets_config_generator.py /ets_config_generator.py
COPY entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

COPY ["default_packages/server_packages.dat", "/root/.local/share/Euro Truck Simulator 2/"]
COPY ["default_packages/server_packages.sii", "/root/.local/share/Euro Truck Simulator 2/"]

ENV LD_LIBRARY_PATH='/app/linux64'

ENTRYPOINT [ "/entrypoint" ]
CMD [ "/app/bin/linux_x64/eurotrucks2_server" ]