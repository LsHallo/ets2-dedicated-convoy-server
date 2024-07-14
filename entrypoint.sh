#!/bin/sh

# Copy default server_packages if they do not exist
cp -n /default_packages/server_packages.sii "${SAVEGAME_LOCATION}"
cp -n /default_packages/server_packages.dat "${SAVEGAME_LOCATION}"

# Generate config and update server
/usr/bin/python3 /ets_server_entrypoint.py

echo "[INFO]: Starting server..."
exec "$@"