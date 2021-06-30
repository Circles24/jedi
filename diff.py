from strategy import (Strategy, StrategyStore)
from exceptions import EmptyDiffStrategy
from constants import (OBJECT_PATH_SEPERATOR, ARRAY_PATH_SEPERATOR, INTERMEDIATE_PERSISTENCE_STRATEGY_KEY)
from logger import logger
from intermediate_persistence import intermediate_persistence_store

class DiffStrategy(Strategy):
    def compute(self, master_schema, branch_schema, context):
        raise EmptyDiffStrategy("empty diff strategy provided")


class FlatCompareStrategy(DiffStrategy):

    def __init__(self):
        self.primitive_json_types = ['int', 'double', 'long', 'string', 'boolean']

    def compute(self, master_schema, branch_schema, context):

        logger.info('using black-magic on schemas')
        path = []

        logger.info('flattening master schema')        
        flat_master_schema = {}
        self.flat_map(master_schema, flat_master_schema, path)

        logger.info('flattening branch schema')
        flat_branch_schema = {}
        self.flat_map(branch_schema, flat_branch_schema, path)

        logger.info('getting intermediate persistence strategy')
        intermediate_persistence_strategy = intermediate_persistence_store.get(context.config[INTERMEDIATE_PERSISTENCE_STRATEGY_KEY])
        intermediate_persistence_strategy.persist(flat_master_schema, flat_branch_schema, context)

        logger.info('computing the diff')
        return self.compare_flat_schema(flat_master_schema, flat_branch_schema)


    def compare_flat_schema(self, flat_master_schema, flat_branch_schema):
        
        master_keys = set(flat_master_schema.keys())
        branch_keys = set(flat_branch_schema.keys())
        common_keys = master_keys.intersection(branch_keys)
        missing_keys = master_keys.difference(common_keys)
        additional_keys = branch_keys.difference(common_keys)

        common_fields = {}
        missing_fields = {}
        additional_fields = {}

        for key in common_keys:
            common_fields[key] = flat_master_schema[key]

        for key in missing_keys:
            missing_fields[key] = flat_master_schema[key]
        
        for key in additional_keys:
            additional_fields[key] = flat_branch_schema[key]

        return common_fields, missing_fields, additional_fields
    

    def persist_response(self, res, path):
        with open(path, 'w') as out_file:
            out_file.write(json.dumps(res, indent=4))


    def flat_map(self, schema, res, path):

        if schema in self.primitive_json_types:
            key = OBJECT_PATH_SEPERATOR.join(path)
            res[key] = schema

        else :
            schema_type = schema['type']

            if schema_type == 'record':
                path.append(schema['name'])
                for field in schema['fields']:
                    self.flat_map(field, res, path)
                path.pop()

            elif schema_type == 'array':
                path.append(ARRAY_PATH_SEPERATOR)
                self.flat_map(schema['items'], res, path)
                path.pop()
            
            if isinstance(schema_type, list):
                assert len(schema_type) == 2
                assert schema_type[0] == "null"
                path.append(schema['name'])
                self.flat_map(schema_type[1], res, path)
                path.pop()

    def get_name(self):
        return 'flat_compare_strategy'

diff_strategy_store = StrategyStore()
diff_strategy_store.bind(FlatCompareStrategy())
