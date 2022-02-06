import json
from strategy import (Strategy, StrategyStore)
from logger import logger
from constants import (ARRAY_PATH_SEPARATOR, OBJECT_PATH_SEPARATOR, JSON_INDENT)

class PersistenceStrategy(Strategy):
    def persist(self, common_fields, missing_fields, additional_fields, context):
        raise EmptyPersistenceStrategy("empty persistence strategy")


class CommonFilePersistenceStrategy(PersistenceStrategy):
    def persist(self, common_fields, missing_fields, additional_fields, context):        
        
        logger.info('using common files persistence strategy')

        merged_response = {"common_fields": common_fields,
                "missing_fields": missing_fields,
                "additional_fields": additional_fields}
        
        diff_schema_path = context.config['diff_schema_path']
        logger.info(f'persisting response into {diff_schema_path}')
        with open(diff_schema_path, 'w') as file_store:
            file_store.write(json.dumps(merged_response, indent=4))
    
    def get_name(self):
        return 'common_file_strategy'


class DiffFilesPersistenceStrategy(PersistenceStrategy):
    def persist(self, common_fields, missing_fields, additional_fields, context):        

        logger.info('using diff files persistence strategy')
        
        common_fields_path = context.config['common_fields_path']
        logger.info(f'persisting common fields in {common_fields_path}')
        with open(common_fields_path, 'w') as file_store:
            file_store.write(json.dumps(common_fields, indent=4))
        
        missing_fields_path = context.config['missing_fields_path']
        logger.info(f'persisting missing fields in {missing_fields_path}')
        with open(missing_fields_path, 'w') as file_store:
            file_store.write(json.dumps(missing_fields, indent=4))

        additional_fields_path = context.config['additional_fields_path']
        logger.info(f'persisting additional fields in {additional_fields_path}')
        with open(additional_fields_path, 'w') as file_store:
            file_store.write(json.dumps(additional_fields, indent=4))


    def get_name(self):
        return 'diff_files_strategy'

class DiffFilesArraySeperationStrategy(PersistenceStrategy):
    def persist(self, common_fields, missing_fields, additional_fields, context):

        logger.info('using diff files with array seperation persistence strategy')
        
        array_seperations = {}
        common_fields = self.seperate_array_fields(common_fields, array_seperations, 'common_fields')
        missing_fields = self.seperate_array_fields(missing_fields, array_seperations, 'missing_fields')
        additional_fields = self.seperate_array_fields(additional_fields, array_seperations, 'additional_fields')

        common_fields_path = context.config['common_fields_path']
        logger.info(f'persisting common fields in {common_fields_path}')
        with open(common_fields_path, 'w') as file_store:
            file_store.write(json.dumps(common_fields, indent=4))
        
        missing_fields_path = context.config['missing_fields_path']
        logger.info(f'persisting missing fields in {missing_fields_path}')
        with open(missing_fields_path, 'w') as file_store:
            file_store.write(json.dumps(missing_fields, indent=4))

        additional_fields_path = context.config['additional_fields_path']
        logger.info(f'persisting additional fields in {additional_fields_path}')
        with open(additional_fields_path, 'w') as file_store:
            file_store.write(json.dumps(additional_fields, indent=4))

        
        for key, value in array_seperations.items():
            with open(f'json_dumps/{key}json', 'w') as file_store:
                logger.info(f'persisting array seperation into json_dumps/{key}json')
                file_store.write(json.dumps(value, indent=4))

    def seperate_array_fields(self, fields, array_fields, field_key):
        
        filtered_fields = {}

        for key, value in fields.items():
            if self.is_array_field(key):
                file_name, file_key = self.get_file_name_and_key(key)
                if file_name not in array_fields: 
                    array_fields[file_name] = {'common_fields':{}, 'missing_fields':{}, 'additional_fields':{}}
                array_fields[file_name][field_key][file_key] = value

            else :
                filtered_fields[key] = value
        return filtered_fields

    def is_array_field(self, path):
        return ARRAY_PATH_SEPARATOR in path

    def get_file_name_and_key(self, path):
        path_list = path.split(ARRAY_PATH_SEPARATOR)
        key = path_list.pop()
        file_name = ARRAY_PATH_SEPARATOR.join(path_list)
        return file_name, key

    def get_name(self):
        return 'diff_files_with_array_seperation_strategy'

 
class DiffFilesArraySeperationNoRootStrategy(PersistenceStrategy):
    def persist(self, common_fields, missing_fields, additional_fields, context):

        logger.info('using diff files with array seperation persistence strategy')
        
        array_seperations = {}
        common_fields = self.seperate_array_fields(common_fields, array_seperations, 'common_fields')
        missing_fields = self.seperate_array_fields(missing_fields, array_seperations, 'missing_fields')
        additional_fields = self.seperate_array_fields(additional_fields, array_seperations, 'additional_fields')

        common_fields_path = context.config['common_fields_path']
        logger.info(f'persisting common fields in {common_fields_path}')
        with open(common_fields_path, 'w') as file_store:
            file_store.write(json.dumps(self.strip_root(common_fields), indent=JSON_INDENT))
        
        missing_fields_path = context.config['missing_fields_path']
        logger.info(f'persisting missing fields in {missing_fields_path}')
        with open(missing_fields_path, 'w') as file_store:
            file_store.write(json.dumps(self.strip_root(missing_fields), indent=JSON_INDENT))

        additional_fields_path = context.config['additional_fields_path']
        logger.info(f'persisting additional fields in {additional_fields_path}')
        with open(additional_fields_path, 'w') as file_store:
            file_store.write(json.dumps(self.strip_root(additional_fields), indent=JSON_INDENT))

        
        for key, value in array_seperations.items():
            for field_type, fields in value.items():
                with open(f'json_dumps/{key}-{field_type}.json', 'w') as file_store:
                    logger.info(f'persisting array seperation into json_dumps/{key}-{field_type}.json')
                    file_store.write(json.dumps(self.strip_root(fields), indent=JSON_INDENT))

    def strip_root(self, fields):
        stripped_fields = {}
        for key, value in fields.items():
            key = key.strip(OBJECT_PATH_SEPARATOR)
            stripped_key = OBJECT_PATH_SEPARATOR.join(key.split(OBJECT_PATH_SEPARATOR)[1::])
            stripped_fields[stripped_key] = value
        return stripped_fields

    def seperate_array_fields(self, fields, array_fields, field_key):
        
        filtered_fields = {}

        for key, value in fields.items():
            if self.is_array_field(key):
                file_name, file_key = self.get_file_name_and_key(key)
                if file_name not in array_fields: 
                    array_fields[file_name] = {'common_fields':{}, 'missing_fields':{}, 'additional_fields':{}}
                array_fields[file_name][field_key][file_key] = value

            else :
                filtered_fields[key] = value
        return filtered_fields

    def is_array_field(self, path):
        return ARRAY_PATH_SEPARATOR in path

    def get_file_name_and_key(self, path):
        path_list = path.split(ARRAY_PATH_SEPARATOR)
        key = path_list.pop()
        file_name = ARRAY_PATH_SEPARATOR.join(path_list)
        return file_name, key

    def get_name(self):
        return 'diff_files_with_array_seperation_no_root_strategy'


class NoPersistenceStrategy(PersistenceStrategy):
    def persist(self, common_fields, missing_fields, additional_fields):
        pass
    
    def get_name(self):
        return 'no_persistence_strategy'

persistence_strategy_store = StrategyStore()
persistence_strategy_store.bind(CommonFilePersistenceStrategy())
persistence_strategy_store.bind(DiffFilesPersistenceStrategy())
persistence_strategy_store.bind(DiffFilesArraySeperationStrategy())
persistence_strategy_store.bind(DiffFilesArraySeperationNoRootStrategy())
persistence_strategy_store.bind(NoPersistenceStrategy())
