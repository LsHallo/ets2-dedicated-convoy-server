`!!This is the README provided with the server download. It is provided here for completeness.!!`


# ATS / ETS2 dedicated server


## 1. Required files to run dedicated server
---
In the game home folder the following files are used to set up dedicated server session:

server_config.sii
 - contains session description and configuration, connections ports info, logon token and list of moderators
 - ports and logon token must be different for each session instance running at the same time
 - default configuration is generated automatically

server_packages.sii
 - contains map details, dlc and mods configuration

server_packages.dat
 - contains internal map data

server_packages.sii and server_packages.dat must be generated manually via calling `export_server_packages` command while normal game is running. Generated dedicated server configuration will be identical to your game configuration when `export_server_packages` command was called. These files are necessary for a dedicated server to start. 


## 2. How to launch a dedicated server
---
You can launch the dedicated server either from the Steam client's Tools tab, or by directly starting its executable. Game ownership is not required. If you want to launch a server with different configuration, use following startup parameters:

 -server "server packages file name"
 -server_cfg "server config file name"

### 2a. How to launch a dedicated server on linux without steam client installed
You may get the following error when starting a server with Linux: `[S_API FAIL] SteamAPI_Init() failed; unable to locate a running instance of Steam, or a local steamclient.dll.`
To launch server on linux `steamclient.so` library is required. You can either use provided launch_server.sh script or create a link to this library using `ln -s steamcmd/linux64/steamclient.so ~/.steam/sdk64/steamclient.so`


## 3. How to export server_packages
---
In config.cfg enable set g_console.
When game is running press `~` to open console and run `export_server_packages` or `export_server_packages destination file` command. server_packages.sii will be generated in the game home folder. It is necessary for map to be loaded when this command is called.


## 4. Data requirements
---
Dedicated server does not require any dlc or mod data. Everything needed is handled via server_packages.sii file. It is not required to copy any additional files. As the dedicated server does not use steam client, it cannot access the workshop.


## 5. Network address translation (NAT)
---
Dedicated server does not handle NAT punching and public IP or port forwarding is required to show server in session browser.
However, session direct search works even for server that is behind NAT and it is possible to connect to such server.

Search id is listed when starting dedicated server or in convoy info screen for hosted sessions.


## 6. Port setup
---
`connection_virtual_port` and `query_virtual_port` are virtual ports used for connection to server. Allowed range is <100,200>.
`connection_dedicated_port` and `query_dedicated_port` are physical ports used by steam game server api to fill sessions browser. For LAN games query_dedicated_port has be in range of <27015,27020>.


## 7. Server logon token
---
By default whenever a dedicated server is launched it is using an anonymous account. For such an account non-persistent server id is generated (used for direct search). To avoid this you can acquire a logon token on https://steamcommunity.com/dev/managegameservers (game ownership is required).


## 8. Session moderators
---
As the dedicated server does not have any form or user interface, it is not possible to promote any player to a moderator while the session is running. You can register moderators in server_config using their steam_id to automatically promote them once they join the session.


## 9. Quality of life
---
Any player who is a moderator can now change the game time. This can be done via chat message box by sending message `/set_time HH:MM'


## 10. How to close server
---
Press Ctrl + C.


## 11. Troubleshooting
---
In game home folder server.log.txt and server.crash.txt (when server crashes) files can be found to help solve any issue with a dedicated server.