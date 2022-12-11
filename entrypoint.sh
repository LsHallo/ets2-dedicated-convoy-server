#!/bin/sh

/usr/bin/python3 /ets_config_generator.py

cp -n /app/default_packages/server_packages.sii "${SAVEGAME_LOCATION}"
cp -n /app/default_packages/server_packages.dat "${SAVEGAME_LOCATION}"

echo "[INFO]: Starting server..."
exec "$@"
echo "[INFO]: Entrypoint done."