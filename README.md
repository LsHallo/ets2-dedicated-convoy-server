# ETS2 Convoy Multiplayer Dedicated Server
This docker container provides the new (as of Dec 2022) dedicated server for ETS2 in a simple and complete package.  
Easy to configure and use!

[GitHub Repo](https://github.com/LsHallo/ets2-dedicated-convoy-server)

# Running
## Minimal example:
```bash
docker run -d --name "ets2-server" \
-v "/opt/ets2:/root/.local/share/Euro Truck Simulator 2" \
-p "27015:27015" -p "27016:27016" \
--restart unless-stopped \
-e "ETS_SERVER_NAME=My Server" \
lshallo/ets2-convoy-server
```
This minimal example will start the server with default settings and a custom name defined.  
It will save the config files to `/opt/ets2`.  

By default the following DLC are enabled:
- Beyond the Baltic Sea
- Going East!
- Vive la France
- Italy
- Scandinavia  

*If you do not own any DLC and can provide me your `server_packages.dat` and `server_packages.sii` that would be a nicer default. Get in touch by opening an [issue](https://github.com/LsHallo/ets2-dedicated-convoy-server/issues) or [pull request](https://github.com/LsHallo/ets2-dedicated-convoy-server/pulls).*

To use you own config see [Custom DLC/Mods](#custom-dlc/mods)

## Docker Compose
```yaml
version: '3'

services:
  ets2-server:
    image: lshallo/ets2-convoy-server
    container_name: ets2-server
    restart: unless-stopped
    ports:
      - "27015:27015"
      - "27016:27016"
    volumes:
      - "/opt/ets2:/root/.local/share/Euro Truck Simulator 2"
    environment:
      - "ETS_SERVER_NAME=My Server"
      - "ETS_SERVER_DESCRIPTION=My server description"
      - "ETS_SERVER_WELCOME_MESSAGE=Welcome to my server!"
      - "ETS_SERVER_PASSWORD=abc123"
      - "ETS_SERVER_MAX_PLAYERS=8"
      - "ETS_SERVER_PORT=27015"
      - "ETS_SERVER_QUERY_PORT=27016"
      # more variables...
```

Then use `docker compose up -d` to start the server.  
You can check the logs with `docker compose logs -f`.

# Server Configuration
## Environment Variables
---
| Variable Name | Example | Description | Default |
| ---------------- | ------------------ | ----------------- | ---------- |
| ETS_SERVER_WRITE_CONFIG | true | Enable/disable automatic config generation from env variables. | true |
| ETS_SERVER_NAME | My Server | The name of the server. Shown ingame. | Euro Truck Simulator 2 Docker Server |
| ETS_SERVER_DESCRIPTION | Join me! | The description of the server. Shown ingame. | "" |
| ETS_SERVER_WELCOME_MESSAGE | Welcome to my server! | The welcome message. Shown ingame. | "" |
| ETS_SERVER_PASSWORD | password | The password required to join your server | "" |
| ETS_SERVER_MAX_PLAYERS | 8 | Max number of players. Probably limited to 8 max. | 8 |
| ETS_SERVER_MAX_VEHICLES_TOTAL | 100 | Maximum number of vehicles on server??? | 100 |
| ETS_SERVER_MAX_AI_VEHICLES_PLAYER | 50 | Maximum number of AI vehicles around a player??? | 50 |
| ETS_SERVER_MAX_AI_VEHICLES_PLAYER_SPAWN | 50 | ??? | 50 |
| ETS_SERVER_CONNECTION_VIRTUAL_PORT | 100 | Virtual connection port. Not used? | 100 |
| ETS_SERVER_QUERY_VIRTUAL_PORT | 101 | Virtual query port. Not used? | 101 |
| ETS_SERVER_PORT | 27015 | The external port of the server. Must be in range 27015 - 27020 | 27015 |
| ETS_SERVER_QUERY_PORT | 27016 | The external query port of the server. Must be in the range 27015 - 2720 | 27016 |
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
| ETS_SERVER_CONFIG_FILE_PATH | /home/user/ets/server_config.sii | Path to server config file. | /root/.local/share/Euro Truck Simulator 2/server_config.sii |

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
    - Restart your server