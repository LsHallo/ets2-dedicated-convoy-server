# ETS2/ATS Convoy Multiplayer Dedicated Server
This docker container provides the new (as of Dec 2022) dedicated server for ETS2/ATS in a simple and complete package.  
Easy to configure and use!

# Contents
 - [Running](#running)
   - [ETS2](#ets2)
   - [ATS](#ats)
 - [Environment Variables](#environment-variables)
 - [Custom DLCs/Mods](#custom-dlcmods)
 - [Troubleshooting](#troubleshooting)
   - [Login Error 15](#login-error-15)
   - [Login Error 106](#login-error-106)
   - [Can't write config file `server_config.sii`](#cant-write-config-file-server_configsii)

# Running
## Minimal example:
### ETS2
```bash
docker run -d \
--name "ets2-server" \
--network host \
--restart unless-stopped \
-e "ETS_SERVER_NAME=My Server" \
lshallo/ets2-convoy-server
```
This minimal example will start the server with default settings and a custom name defined.  

By default the following DLC are enabled:
- Beyond the Baltic Sea
- Going East!
- Vive la France
- Italy
- Scandinavia  

These seem not to be required to join.  
*If you do not own any DLC and can provide me your `server_packages.dat` and `server_packages.sii` that would be a nicer default. Get in touch by opening an [issue](https://github.com/LsHallo/ets2-dedicated-convoy-server/issues) or [pull request](https://github.com/LsHallo/ets2-dedicated-convoy-server/pulls).*

To use your own config see [Custom DLC/Mods](#custom-dlcmods)

---
### ATS
```bash
docker run -d \
--name "ats-server" \
--network host \
--restart unless-stopped \
-e "ETS_SERVER_NAME=My Server" \
lshallo/ats-convoy-server
```
This minimal example will start the server with default settings and a custom name defined.  

By default the following DLC are enabled:
- Arizona
- Nevada

To use your own config see [Custom DLC/Mods](#custom-dlcmods)


## Docker Compose
See [docker-compose.yml](docker-compose.yml).

Then use `docker compose up -d` to start the server.  
You can check the logs with `docker compose logs -f`.

Update the server with `docker compose pull && docker compose up -d`.
Stop the server with `docker compose stop` and remove it with `docker compose down`.

# Server Configuration
## Environment Variables
---
| Variable Name | Example | Description | Default |
| ---------------- | ------------------ | ----------------- | ---------- |
| ETS_SERVER_WRITE_CONFIG | true | Enable/disable automatic config generation from env variables. | true |
| ETS_SERVER_UPDATE_ON_START | true | Enable/disable update on server start. Will always update on first start to get server files. | true |
| ETS_SERVER_NAME | My Server | The name of the server. Shown ingame. | Euro Truck Simulator 2 Docker Server |
| ETS_SERVER_DESCRIPTION | Join me! | The description of the server. Shown ingame. | "" |
| ETS_SERVER_WELCOME_MESSAGE | Welcome to my server! | The welcome message. Shown ingame. | "" |
| ETS_SERVER_PASSWORD | password | The password required to join your server | "" |
| ETS_SERVER_MAX_PLAYERS | 8 | Max number of players. Probably limited to 8 max. | 8 |
| ETS_SERVER_MAX_VEHICLES_TOTAL | 100 | Maximum number of vehicles on server??? | 100 |
| ETS_SERVER_MAX_AI_VEHICLES_PLAYER | 50 | Maximum number of AI vehicles around a player??? | 50 |
| ETS_SERVER_MAX_AI_VEHICLES_PLAYER_SPAWN | 50 | ??? | 50 |
| ETS_SERVER_CONNECTION_VIRTUAL_PORT | 100 | Virtual connection port. Only used internally. Do not forward. | 100 |
| ETS_SERVER_QUERY_VIRTUAL_PORT | 101 | Virtual query port. Only used internally. Do not forward. | 101 |
| ETS_SERVER_PORT | 27015 | The external port of the server. You need to forward UDP + TCP. | 27015 |
| ETS_SERVER_QUERY_PORT | 27016 | The external query port of the server. You need to forward UDP + TCP. Must be in the range 27015 - 2720 for LAN games. | 27016 |
| ETS_SERVER_LOGON_TOKEN | 79gzbtepa2f0q72grfvazhhpsdasd | The logon token to have a persistent search token. See [Server README](ETS_SERVER_README.md#7-server-logon-token) | "" |
| ETS_SERVER_PLAYER_DAMAGE | true | Enable/disable player collisions | true |
| ETS_SERVER_TRAFFIC | true | Enable/disable traffic | true |
| ETS_SERVER_HIDE_IN_COMPANY | false | Enable/disable collisions of players in menu | false |
| ETS_SERVER_HIDE_COLLIDING | true | Enable/disable hiding of players in no collisions zone | true |
| ETS_SERVER_FORCE_SPEEDLIMITER | false | Enable/disable speed limit | false |
| ETS_SERVER_MODS_OPTIONING | false | Enable optional mods | false |
| ETS_SERVER_SERVICE_NO_COLLISION | false | Enable/disable collision in service areas (true = collisions enable, false = collisions disabled) | false |
| ETS_SERVER_NAME_TAGS | true | Enable/disable display of name tags above trucks | true |
| ETS_SERVER_FRIENDS_ONLY | false | Limit server to steam friends??? | false |
| ETS_SERVER_SHOW_SERVER | true | Show server in public server list? | true |
| ETS_SERVER_MODERATORS | 208370238402, 2384723894723, 283947923 | List of steam IDs to turn moderatos on join. Moderators can alter the server time. See [Server README](ETS_SERVER_README.md#8-session-moderators) | "" |
| ETS_SERVER_CONFIG_FILE_PATH | /home/user/ets/server_config.sii | Path to server config file. | /home/steam/.local/share/Euro Truck Simulator 2/server_config.sii |
| ETS_SERVER_BRANCH | temporary_1_47 | Server branch. Allows downgrading to an older version. At SteamDB you'll find available branches for both [ETS2](https://steamdb.info/app/1948160/depots) and [ATS](https://steamdb.info/app/2239530/depots). To return back to the latest public release, use "public" | "" |

*As you can probably tell, there are some question marks in the descriptions. I'm not sure what the parameters are doing. If you have any clue, please open an [issue](https://github.com/LsHallo/ets2-dedicated-convoy-server/issues) or [pull request](https://github.com/LsHallo/ets2-dedicated-convoy-server/pulls).*


## Custom DLC/Mods
---
To enable your installed DLCs or mods you need to generate custom `server_packages.dat` and `server_packages.sii` files.

1. Locate your ETS2 savegames folder
    - Windows: `%USERPROFILE%\Documents\Euro Truck Simulator 2`
    - Mac: 
        - No Steam Cloud: `~/Library/Application Support/Euro Truck Simulator 2/profiles/<Your Profile>/save`
        - Steam Cloud: `~/Library/Application Support/Steam/userdata/<Your ID>/304730/remote/profiles/<Your Profile>/save`
    - Linux: You know best ;)
  
  
2. Open `config.cfg` in your favourite editor (Notepad++, Emacs, Vim, ...)
    - Search for `uset g_console "0"` and replace it with `uset g_console "1"`
    - Search for `uset g_developer "0"` and replace it with `uset g_developer "1"`
    - Save the file

3. Start the game and load your desired save. The state (where your truck is) of the save is not important we will only export mods and DLC.
    - Open the console by pressing the `~` key (left of 1 in the number row). It will vary depending on your keyboard layout.
    - Type `export_server_packages` in the console at the bottom of the screen and press enter.

4. Go to your savegames folder again.
    - You should see 2 new files: `server_packages.dat` and `server_packages.sii`
    - Copy the files to your ets2 server data directory (replacing the existing ones)
        - You need to mount `/home/steam/.local/share/Euro Truck Simulator 2` to a local directory using your docker run config.
        - Place the files in the mounted directory. E.g.: `/opt/ets2`
    - Restart your server



# Troubleshooting


## Login Error 15
Login error 15 indicates that the token is for the wrong game. Please check that you have not used your ETS token for ATS or similar.  

See [ETS_SERVER_README.md](ETS_SERVER_README.md#7-server-logon-token) to genrate a new token.


## Login Error 106
Login error 106 indicates that your logon token is invalid.  
The token will lose validity after some time and you will need to generate a new one.  
To check if the token is still valid log into steam in a browser and go to [https://steamcommunity.com/dev/managegameservers](https://steamcommunity.com/dev/managegameservers).  
If the token has strike through it is no longer valid.  

See [ETS_SERVER_README.md](ETS_SERVER_README.md#7-server-logon-token) to genrate a new token.


## Can't write config file `server_config.sii`
Make sure the mounted folder owner is user id 1000.
`chown -R 1000:1000 /opt/ets2` (or whereever you have mounted it)