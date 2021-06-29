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
            self.context = context
            logger.info('jedi initialized now u can use its black-magic')
        else :
            error = 'expected context object in jedi __init__'
            logger.error(error)
            raise InvalidJediArgPassed(error)

    def execute(self):
        logger.info('using black-magic on schemas')
        
        logger.info('computing diff')
        common_fields, missing_fields, additional_fields = self.context.diff_strategy.compute(self.master_schema, self.branch_schema)
        logger.info('computed the diff')

        logger.info('persisting the result')
        self.context.persistence_strategy.persist(common_fields, missing_fields, additional_fields, self.context)
        logger.info('persisted the result')

        logger.info('yo yo yo xoxox jedi is done')
