import json


class ConfigProvider:
    """Class to load and 'provide' config file"""
    def __init__(self):
        """Inside the init method we call the private load config method"""
        print('Init config')
        self.__config = self.__load_config('config.json')

    def __load_config(self, config_name: str) -> dict:
        """Load json config file """
        with open(config_name, "r") as f:
            config = json.load(f)

        return config

    def get_property(self, property_name: str):
        """Method to get a property from configuration file. If property is not set None is returned and warning is printed"""
        try:
            return self.__config[property_name]
        except Exception as err:
            print(f"Property: {property_name} not defined")
            return None
