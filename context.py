import os
import json
from logger import logger
from exceptions import (ContextBuildingException, InvalidConfigException)

DEFAULT_CONFIG_PATH = 'config.json'

class Context:
    mandatory_existing_keys = ['master_schema_path', 'branch_schema_path']
    mandatory_optional_keys = ['flat_master_schema_path', 'flat_branch_schema_path','diff_schema_path']

    def __init__(self):
        try:
            logger.info('building context')
            config_path = os.getenv('CONFIG_PATH')
            if config_path is None:
                config_path = DEFAULT_CONFIG_PATH
            logger.info(f'using {config_path} as config path')
            with open(config_path, 'r') as config_file:
                raw_config = config_file.read()
                self.config = json.loads(raw_config)
            for mandatory_key in self.mandatory_existing_keys:
                if mandatory_key not in self.config:
                    error = f'mandatory key missing in config :: {mandatory_key}'
                    logger.error(error)
                    raise InvalidConfigException(error)
                elif os.path.exists(self.config[mandatory_key]) == False:
                    error = f'json schema missing :: {self.config[mandatory_key]}'
                    logger.error(error)
                    raise InvalidConfigException(error)


            for mandatory_key in self.mandatory_optional_keys:
                if mandatory_key not in self.config:
                    error = f'mandatory key missing in config :: {mandatory_key}'
                    logger.error(error)
                    raise InvalidConfigException(error)

        except Exception as ex:
            error = f'error while building context for app :: {ex}'
            logger.error(error)
            raise ContextBuildingException(error)

