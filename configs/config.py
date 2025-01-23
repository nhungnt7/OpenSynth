from configs.config_loader import ConfigReaderInstance

class Config:
    """Returns a config instance depending on the ENV_STATE variable."""
    def __init__(self, args=None):
        try:
            if args.override_default_config:
                settings_params = args.override_default_config
            else:
                settings_params = "settings/config.yml"
        except:
            settings_params = "settings/config.yml"

        self.CONF = ConfigReaderInstance.yaml.read_config_from_file(settings_params)


def set_config(args=None):
    global settings
    settings = Config(args)
