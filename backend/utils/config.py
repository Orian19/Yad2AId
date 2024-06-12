import json


def load_config(cfg_file=r'scraping_cfg.json'):
    """
    loading the json config
    :param cfg_file:
    :return:
    """
    with open(cfg_file) as config_file:
        return json.load(config_file)
