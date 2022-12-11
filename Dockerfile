FROM steamcmd/steamcmd:ubuntu

ARG APP_ID=1948160
ARG SAVEGAME_LOCATION="/root/.local/share/Euro Truck Simulator 2/"
ARG EXECUTABLE="/app/bin/linux_x64/eurotrucks2_server"
ARG DEFAULT_PACKAGES="default_packages/ets2"

ENV SAVEGAME_LOCATION="${SAVEGAME_LOCATION}"
ENV ETS_SERVER_CONFIG_FILE_PATH="${SAVEGAME_LOCATION}server_config.sii"
ENV EXECUTABLE=${EXECUTABLE}

WORKDIR /app

RUN steamcmd +force_install_dir /app +login anonymous +app_update ${APP_ID} +quit

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y nano python3 \
    && mkdir -p "${SAVEGAME_LOCATION}" \
    && mkdir -p /app/default_packages

COPY ets_config_generator.py /ets_config_generator.py
COPY entrypoint.sh /entrypoint
RUN chmod +x /entrypoint

COPY ["${DEFAULT_PACKAGES}/server_packages.dat", "/app/default_packages/"]
COPY ["${DEFAULT_PACKAGES}/server_packages.sii", "/app/default_packages/"]

ENV LD_LIBRARY_PATH='/app/linux64'

ENTRYPOINT [ "/entrypoint" ]
CMD [ "${EXECUTABLE}" ]