from context import Context
from jedi import Jedi
from logger import logger
from exceptions import ContextBuildingException

def __main__():
    try:
        app_context = Context()
        jedi = Jedi(app_context)
        jedi.execute()
    except Exception as ex:
        logger.error(f'unfortunate are those who coudnt witness black-magic')
        logger.error(f'jedi couldnt be summoned :: {ex}')

if __name__ == '__main__':
    logger.info('yo starting jedi app')
    __main__()
