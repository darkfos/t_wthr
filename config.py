from configparser import ConfigParser

config = ConfigParser()
config.read("weather_configs.ini")

API_KEY = config.get("auth", "API_KEY")
TG_API_KEY = config.get("auth", "TG_API_KEY")