OBJECT_PATH_SEPERATOR = '.'
ARRAY_PATH_SEPERATOR = '|'
DEFAULT_CONFIG_PATH = 'config.json'
MANDATORY_EXISTING_PATH_KEYS = ['master_schema_path', 'branch_schema_path']
MANDATORY_OPTIONAL_PATH_KEYS = ['flat_master_schema_path', 'flat_branch_schema_path', 'diff_schema_path', 'common_fields_path',
        'missing_fields_path', 'additional_fields_path']
DIFF_STRATEGIES = ['flat_compare']
DIFF_STRATEGY_KEY = 'diff_strategy'
PERSISTENCE_STRATEGIES = ['common_file', 'diff_files', 'diff_files_with_array_speration']
PERSISTENCE_STRATEGY_KEY = 'persistence_strategy'