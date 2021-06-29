import os
import json
from logger import logger
from exceptions import (ContextBuildingException, InvalidConfigException, InvalidDiffStrategy, InvalidPersistenceStrategy)
from constants import (DEFAULT_CONFIG_PATH, MANDATORY_EXISTING_PATH_KEYS, MANDATORY_OPTIONAL_PATH_KEYS, 
        DIFF_STRATEGIES, PERSISTENCE_STRATEGIES, DIFF_STRATEGY_KEY, PERSISTENCE_STRATEGY_KEY)

class Context:

    def __init__(self, diff_strategy_store, persistence_strategy_store):
        try:
            logger.info('building context')
            config_path = os.getenv('CONFIG_PATH')
            if config_path is None:
                config_path = DEFAULT_CONFIG_PATH
            logger.info(f'using {config_path} as config path')
            with open(config_path, 'r') as config_file:
                raw_config = config_file.read()
                self.config = json.loads(raw_config)
            for mandatory_key in MANDATORY_EXISTING_PATH_KEYS:
                if mandatory_key not in self.config:
                    error = f'mandatory key missing in config :: {mandatory_key}'
                    logger.error(error)
                    raise InvalidConfigException(error)
                elif os.path.exists(self.config[mandatory_key]) == False:
                    error = f'json schema missing :: {self.config[mandatory_key]}'
                    logger.error(error)
                    raise InvalidConfigException(error)

            for mandatory_key in MANDATORY_OPTIONAL_PATH_KEYS:
                if mandatory_key not in self.config:
                    error = f'mandatory key missing in config :: {mandatory_key}'
                    logger.error(error)
                    raise InvalidConfigException(error)
            
            self.diff_strategy = diff_strategy_store.get(self.config[DIFF_STRATEGY_KEY])
            self.persistence_strategy = persistence_strategy_store.get(self.config[PERSISTENCE_STRATEGY_KEY])

        except Exception as ex:
            error = f'error while building context for app :: {ex}'
            logger.error(error)
            raise ContextBuildingException(error)

