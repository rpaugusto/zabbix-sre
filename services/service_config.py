#services/service_config

import os
from dotenv import dotenv_values

ENV_PATH = ".env"

def load_env():
    return dotenv_values(ENV_PATH)


def update_env(zabbix_url: str, zabbix_token: str | None):
    current = dotenv_values(ENV_PATH)

    if zabbix_url:
        current["ZABBIX_URL"] = zabbix_url

    if zabbix_token:
        current["ZABBIX_API_TOKEN"] = zabbix_token

    with open(ENV_PATH, "w") as f:
        for k, v in current.items():
            if v is not None:
                f.write(f"{k}={v}\n")
