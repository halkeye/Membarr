import configparser
import os
from os import path
from dotenv import load_dotenv

load_dotenv(dotenv_path='bot.env')

CONFIG_PATH = 'app/config/config.ini'
BOT_SECTION = 'bot_envs'
MEMBARR_VERSION = 1.1

config = configparser.ConfigParser(os.environ)

CONFIG_KEYS = ['username', 'password', 'discord_bot_token', 'plex_user', 'plex_pass', 'plex_token',
                'plex_base_url', 'plex_roles', 'plex_server_name', 'plex_libs', 'owner_id', 'channel_id',
                'auto_remove_user', 'jellyfin_api_key', 'jellyfin_server_url', 'jellyfin_roles',
                'jellyfin_libs', 'plex_enabled', 'jellyfin_enabled', 'jellyfin_external_url']

# settings
Discord_bot_token = ""
plex_roles = None
PLEXUSER = ""
PLEXPASS = ""
PLEX_SERVER_NAME = ""
PLEX_TOKEN = ""
PLEX_BASE_URL = ""
Plex_LIBS = None
JELLYFIN_SERVER_URL = ""
JELLYFIN_API_KEY = ""
jellyfin_libs = ""
jellyfin_roles = None
plex_configured = True
jellyfin_configured = True

if not (path.exists(CONFIG_PATH)):
    with open (CONFIG_PATH, 'w') as fp:
        pass



config.read(CONFIG_PATH)

plex_token_configured = True
try:
    PLEX_TOKEN = config.get(BOT_SECTION, 'plex_token')
    PLEX_BASE_URL = config.get(BOT_SECTION, 'plex_base_url')
except (configparser.NoSectionError, KeyError) as e:
    print("No Plex auth token details found", e)
    plex_token_configured = False

# Get Plex config
try:
    PLEX_SERVER_NAME = config.get(BOT_SECTION, 'plex_server_name')
    PLEXUSER = config.get(BOT_SECTION, 'plex_user')
    PLEXPASS = config.get(BOT_SECTION, 'plex_pass')
except (configparser.NoSectionError, KeyError) as e:
    print("No Plex login info found", e)
    if not plex_token_configured:
        print("Could not load plex config")
        plex_configured = False

# Get Plex roles config
try:
    plex_roles = config.get(BOT_SECTION, 'plex_roles')
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Plex roles config", e)
    plex_roles = None
if plex_roles:
    plex_roles = list(plex_roles.split(','))
else:
    plex_roles = []

# Get Plex libs config
try:
    Plex_LIBS = config.get(BOT_SECTION, 'plex_libs')
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Plex libs config. Defaulting to all libraries.", e)
    Plex_LIBS = None
if Plex_LIBS is None:
    Plex_LIBS = ["all"]
else:
    Plex_LIBS = list(Plex_LIBS.split(','))
    
# Get Jellyfin config
try:
    JELLYFIN_SERVER_URL = config.get(BOT_SECTION, 'jellyfin_server_url')
    JELLYFIN_API_KEY = config.get(BOT_SECTION, "jellyfin_api_key")
except (configparser.NoSectionError, KeyError) as e:
    print("Could not load Jellyfin config", e)
    jellyfin_configured = False

try:
    JELLYFIN_EXTERNAL_URL = config.get(BOT_SECTION, "jellyfin_external_url")
    if not JELLYFIN_EXTERNAL_URL:
        JELLYFIN_EXTERNAL_URL = JELLYFIN_SERVER_URL
except (configparser.NoSectionError, KeyError) as e:
    JELLYFIN_EXTERNAL_URL = JELLYFIN_SERVER_URL
    print("Could not get Jellyfin external url. Defaulting to server url.", e)

# Get Jellyfin roles config
try:
    jellyfin_roles = config.get(BOT_SECTION, 'jellyfin_roles')
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Jellyfin roles config", e)
    jellyfin_roles = None
if jellyfin_roles:
    jellyfin_roles = list(jellyfin_roles.split(','))
else:
    jellyfin_roles = []

# Get Jellyfin libs config
try:
    jellyfin_libs = config.get(BOT_SECTION, 'jellyfin_libs')
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Jellyfin libs config. Defaulting to all libraries.", e)
    jellyfin_libs = None
if jellyfin_libs is None:
    jellyfin_libs = ["all"]
else:
    jellyfin_libs = list(jellyfin_libs.split(','))

# Get Enable config
try:
    USE_JELLYFIN = config.get(BOT_SECTION, 'jellyfin_enabled')
    USE_JELLYFIN = USE_JELLYFIN.lower() == "true"
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Jellyfin enable config. Defaulting to False", e)
    USE_JELLYFIN = False

try:
    USE_PLEX = config.get(BOT_SECTION, "plex_enabled")
    USE_PLEX = USE_PLEX.lower() == "true"
except (configparser.NoSectionError, KeyError) as e:
    print("Could not get Plex enable config. Defaulting to False", e)
    USE_PLEX = False

def get_config():
    """
    Function to return current config
    """
    try:
        config.read(CONFIG_PATH)
        return config
    except Exception as e:
        print(e)
        print('error in reading config')
        return None


def change_config(key, value):
    """
    Function to change the key, value pair in config
    """
    try:
        config.set(BOT_SECTION, key, str(value))
    except (configparser.NoSectionError, KeyError) as _:
        config.add_section(BOT_SECTION)
        config.set(BOT_SECTION, key, str(value))

    try:
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(e)
        print("Cannot write to config.")
