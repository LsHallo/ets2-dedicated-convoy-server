#!/bin/sh

# Generate config and update server
# I can't bash so I wrote a python script
/usr/bin/python3 /ets_server_entrypoint.py

# Copy default server_packages if they do not exist
cp -n /default_packages/server_packages.sii "${SAVEGAME_LOCATION}"
cp -n /default_packages/server_packages.dat "${SAVEGAME_LOCATION}"

echo "[INFO]: Starting server..."
exec "$@"