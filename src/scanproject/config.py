import json
import pathlib


def load():
    cwd = pathlib.Path(__file__).parent
    config_path = cwd / "config.json"

    if config_path.exists():
        with open(config_path, "r") as fp:
            config_dict = json.load(fp)
    else:
        config_dict = {"model": "gpt-3.5-turbo"}

    return config_dict


def save(new_config):
    cwd = pathlib.Path(__file__).parent
    config_path = cwd / "config.json"

    with open(config_path, "w") as fp:
        json.dump(new_config, fp)
