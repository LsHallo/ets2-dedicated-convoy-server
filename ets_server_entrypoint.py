#!/usr/bin/python3

import os
import os.path


def server_files_exist() -> bool:
    """
    Checks if the main server executable is present.
    Uses env variable `EXECUTABLE` as path to check.
    """
    executable_path = os.getenv("EXECUTABLE")
    return os.path.isfile(executable_path)


def generate_moderator_list(mod_list: list) -> str:
    """
    Generates the string required by the server_config.sii file.
    Example:
    ```python
    >>> print(generate_moderator_list(["1028371289", "1247129874"]))
    moderator_list: 2
    moderator_list[0]: 1028371289
    moderator_list[1]: 1247129874
    ```
    """

    if len(mod_list) == 1 and len(mod_list[0]) < 1:
        return "moderator_list: 0"
    
    out_str = f"moderator_list: {len(mod_list)}\n"
    for i, mod in enumerate(mod_list):
        out_str += f" moderator_list[{i}]: {str(mod).strip()}\n"
    
    return out_str


def is_truthy(any_str: str) -> bool:
    """
    Returns True if str is "yes", "true", "on" or "1".
    Case insensitive.
    """
    if any_str.lower() in ["yes", "true", "on", "1"]:
        return True
    return False


def generate_config() -> str:
    """
    Generates the config file based on environment variables.
    Conforms to SCS scheme (that is sadly not published...).
    """
    print("[INFO]: Writing config file...")

    server_name = os.getenv("ETS_SERVER_NAME", "Euro Truck Simulator 2 Docker Server")
    description = os.getenv("ETS_SERVER_DESCRIPTION", "")
    welcome_message = os.getenv("ETS_SERVER_WELCOME_MESSAGE", "")
    password = os.getenv("ETS_SERVER_PASSWORD", "")
    max_players = os.getenv("ETS_SERVER_MAX_PLAYERS", "8")
    max_vehicles_total = os.getenv("ETS_SERVER_MAX_VEHICLES_TOTAL", "100")
    max_ai_vehicles_player = os.getenv("ETS_SERVER_MAX_AI_VEHICLES_PLAYER", "50")
    max_ai_vehicles_player_spawn = os.getenv("ETS_SERVER_MAX_AI_VEHICLES_PLAYER_SPAWN", "50")
    connection_virtual_port = os.getenv("ETS_SERVER_CONNECTION_VIRTUAL_PORT", "100")
    query_virtual_port = os.getenv("ETS_SERVER_QUERY_VIRTUAL_PORT", "101")
    server_port = os.getenv("ETS_SERVER_PORT", "27015")
    query_port = os.getenv("ETS_SERVER_QUERY_PORT", "27016")
    server_logon_token = os.getenv("ETS_SERVER_LOGON_TOKEN", "")
    player_damage = is_truthy(os.getenv("ETS_SERVER_PLAYER_DAMAGE", "true"))
    traffic = is_truthy(os.getenv("ETS_SERVER_TRAFFIC", "true"))
    hide_in_company = is_truthy(os.getenv("ETS_SERVER_HIDE_IN_COMPANY", "false"))
    hide_colliding = is_truthy(os.getenv("ETS_SERVER_HIDE_COLLIDING", "true"))
    force_speedlimiter = is_truthy(os.getenv("ETS_SERVER_FORCE_SPEEDLIMITER", "false"))
    mods_optioning = is_truthy(os.getenv("ETS_SERVER_MODS_OPTIONING", "false"))
    timezones = is_truthy(os.getenv("ETS_SERVER_TIMEZONES", "false"))
    service_no_collision = is_truthy(os.getenv("ETS_SERVER_SERVICE_NO_COLLISION", "false"))
    in_menu_ghosting = is_truthy(os.getenv("ETS_SERVER_IN_MENU_GHOSTING", "false"))
    name_tags = is_truthy(os.getenv("ETS_SERVER_NAME_TAGS", "true"))
    friends_only = is_truthy(os.getenv("ETS_SERVER_FRIENDS_ONLY", "false"))
    show_server = is_truthy(os.getenv("ETS_SERVER_SHOW_SERVER", "true"))
    moderator_list = os.getenv("ETS_SERVER_MODERATORS", "").split(",")
    moderator_list_generated = generate_moderator_list(moderator_list)

# This is ugly AF but if you indent it differently it breaks the config...
    server_config = f"""SiiNunit
{{
server_config : _nameless.44c.eab0 {{
 lobby_name: "{server_name}"
 description: "{description}"
 welcome_message: "{welcome_message}"
 password: "{password}"
 max_players: {int(max_players)}
 max_vehicles_total: {int(max_vehicles_total)}
 max_ai_vehicles_player: {int(max_ai_vehicles_player)}
 max_ai_vehicles_player_spawn: {int(max_ai_vehicles_player_spawn)}
 connection_virtual_port: {int(connection_virtual_port)}
 query_virtual_port: {int(query_virtual_port)}
 connection_dedicated_port: {int(server_port)}
 query_dedicated_port: {int(query_port)}
 server_logon_token: "{server_logon_token}"
 player_damage: {str(player_damage).lower()}
 traffic: {str(traffic).lower()}
 hide_in_company: {str(hide_in_company).lower()}
 hide_colliding: {str(hide_colliding).lower()}
 force_speed_limiter: {str(force_speedlimiter).lower()}
 mods_optioning: {str(mods_optioning).lower()}
 timezones: {int(timezones)}
 service_no_collision: {str(service_no_collision).lower()}
 in_menu_ghosting: {str(in_menu_ghosting).lower()}
 name_tags: {str(name_tags).lower()}
 friends_only: {str(friends_only).lower()}
 show_server: {str(show_server).lower()}
 {moderator_list_generated}
}}
}}
"""

    return server_config


if __name__ == "__main__":
    if is_truthy(os.getenv("ETS_SERVER_WRITE_CONFIG", "true")):
        config = generate_config()
        config_path = os.getenv("ETS_SERVER_CONFIG_FILE_PATH", "/home/steam/.local/share/Euro Truck Simulator 2/server_config.sii")
        with open(config_path, "w") as f:
            if f.writable():
                f.write(config)
                f.flush()
                print("[INFO]: Config file written.")
            else:
                print(f"[ERROR]: Could not write config file ({config_path}). Check file permissions!")

    if is_truthy(os.getenv("ETS_SERVER_UPDATE_ON_START", "true")) or not server_files_exist():
        print("[INFO]: Updating ETS Server...")
        APP_ID = os.getenv("APP_ID")
        beta_argument = " -beta " + os.getenv("ETS_SERVER_BRANCH") if os.getenv("ETS_SERVER_BRANCH") else ""
        os.system(f"/home/steam/steamcmd/steamcmd.sh +force_install_dir /app +login anonymous +app_update {APP_ID}{beta_argument} +quit")
        print("[INFO]: Update done.")
    else:
        print("[INFO]: Skipping server update. To update set 'ETS_SERVER_UPDATE_ON_START=true'.")
