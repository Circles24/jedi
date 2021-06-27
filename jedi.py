import json
import pdb
import traceback
from context import Context
from exceptions import InvalidJediArgPassed
from logger import logger


class Jedi:
    def __init__(self, context):
        
        self.primitive_json_types = ['int', 'long', 'double', 'string', 'boolean']

        if isinstance(context, Context):
            logger.info('building jedi instance')
            self.master_schema = json.loads(open(context.config['master_schema_path']).read())
            self.branch_schema = json.loads(open(context.config['branch_schema_path']).read())
            self.flat_master_schema_path = context.config['flat_master_schema_path']
            self.flat_branch_schema_path = context.config['flat_branch_schema_path']
            self.diff_schema_path = context.config['diff_schema_path']
            logger.info('jedi initialized now u can use its black-magic')
        else :
            error = 'expected Context object in jedi __init__'
            logger.error(error)
            raise InvalidJediArgPassed(error)

    def execute(self):
        logger.info('using black-magic on schemas')
        path = []

        master_schema = self.master_schema
        branch_schema = self.branch_schema

        logger.info('flattening master schema')        
        flat_master_schema = {}
        self.flat_map(master_schema, flat_master_schema, path)
        self.persist_response(flat_master_schema, self.flat_master_schema_path)

        logger.info('flattening branch schema')
        flat_branch_schema = {}
        self.flat_map(branch_schema, flat_branch_schema, path)
        self.persist_response(flat_branch_schema, self.flat_branch_schema_path)
        
        logger.info('computing the diff')
        res = self.compare_flat_schema(flat_master_schema, flat_branch_schema)

        logger.info('jedi is done now')
        logger.info(f'persisting response into {self.diff_schema_path}')
        self.persist_response(res, self.diff_schema_path)
        logger.info('done with persisting :)')


    def compare_flat_schema(self, flat_master_schema, flat_branch_schema):
        res = {'common_fields':[], 'missing_fields':[], 'additional_fields':[]}
        
        master_keys = set(flat_master_schema.keys())
        branch_keys = set(flat_branch_schema.keys())
        common_keys = master_keys.intersection(branch_keys)
        missing_keys = master_keys.difference(common_keys)
        additional_keys = branch_keys.difference(common_keys)

        for key in common_keys:
            res['common_fields'].append({key: flat_master_schema[key]})

        for key in missing_keys:
            res['missing_fields'].append({key: flat_master_schema[key]})
        
        for key in additional_keys:
            res['additional_fields'].append({key: flat_branch_schema[key]})

        return res
        


    def persist_response(self, res, path):
        with open(path, 'w') as out_file:
            out_file.write(json.dumps(res, indent=4))


    def flat_map(self, schema, res, path):
        # pdb.set_trace()

        if schema in self.primitive_json_types:
            key = '.'.join(path)
            res[key] = schema

        else :
            schema_type = schema['type']

            if schema_type == 'record':
                path.append(schema['name'])
                for field in schema['fields']:
                    self.flat_map(field, res, path)
                path.pop()

            elif schema_type == 'array':
                path.append("|")
                self.flat_map(schema['items'], res, path)
                path.pop()
            
            if isinstance(schema_type, list):
                assert len(schema_type) == 2
                assert schema_type[0] == "null"
                path.append(schema['name'])
                self.flat_map(schema_type[1], res, path)
                path.pop()
