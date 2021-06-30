import json
from strategy import (Strategy, StrategyStore)
from constants import (JSON_INDENT, COMMON_INTERMEDIATE_PATH_KEY, MASTER_INTERMEDIATE_PATH_KEY, BRANCH_INTERMEDIATE_PATH_KEY)
from logger import logger

class IntermediatePersistenceStrategy(Strategy):
    def persist(self, flat_master_schema, flat_branch_schema):
        raise InvalidIntermediatePersistenceStrategy

class CommonFileIntermediatePersistenceStrategy(IntermediatePersistenceStrategy):
    def persist(self, flat_master_schema, flat_branch_schema, context):
        logger.info('using common file intermediate strategy')

        flat_common_path = context.config[COMMON_INTERMEDIATE_PATH_KEY]
        logger.info(f'persisting flat common schema in {flat_common_path}')
        common_flat_schema = {"flat_master_schema":flat_master_schema, "flat_branch_schema":flat_branch_schema}
        with open(flat_common_path, 'w') as file_store:
            file_store.write(json.dumps(common_flat_schema, indent=JSON_INDENT))

    def get_name(self):
        return 'common_file_intermediate_persistence_strategy'


class DiffFilesIntermediatePersistenceStrategy(IntermediatePersistenceStrategy):
    def persist(self, flat_master_schema, flat_branch_schema, context):
        logger.info('using diff files intermediate persistence strategy')

        flat_master_path = context.config[MASTER_INTERMEDIATE_PATH_KEY]
        logger.info(f'persisting flat master schema in {flat_master_path}')
        with open(flat_master_path, 'w') as file_store:
            file_store.write(json.dumps(flat_master_schema, indent=JSON_INDENT))
        
        flat_branch_path = context.config[BRANCH_INTERMEDIATE_PATH_KEY]
        logger.info(f'persisting flat branch schema in {flat_branch_path}')
        with open(flat_branch_path, 'w') as file_store:
            file_store.write(json.dumps(flat_branch_schema, indent=JSON_INDENT))

    def get_name(self):
        return 'diff_files_intermediate_persistence_strategy'


class NoIntermediatePersistenceStrategy(IntermediatePersistenceStrategy):
    def persist(self, flat_master_schema, flat_branch_schema, context):
        pass
    def get_name(self):
        return 'no_intermediate_persistence_strategy'


intermediate_persistence_store = StrategyStore()
intermediate_persistence_store.bind(CommonFileIntermediatePersistenceStrategy())
intermediate_persistence_store.bind(DiffFilesIntermediatePersistenceStrategy())
intermediate_persistence_store.bind(NoIntermediatePersistenceStrategy())
