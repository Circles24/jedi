from context import Context
from jedi import Jedi
from logger import logger
from diff import diff_strategy_store
from persistence import persistence_strategy_store
from traceback import print_exc


def __main__():
    try:
        app_context = Context(diff_strategy_store, persistence_strategy_store)
        jedi = Jedi(app_context)
        jedi.execute()
    except Exception as ex:
        print_exc()
        logger.error(f'unfortunate are those who could not witness black-magic')
        logger.error(f'jedi could not be summoned :: {ex}')


if __name__ == '__main__':
    logger.info('starting jedi app')
    __main__()
