class Strategy:
    def get_name(self):
        pass


class StrategyStore:

    def __init__(self):
        self.store = {}

    def bind(self, strategy):
        assert isinstance(strategy, Strategy)
        self.store[strategy.get_name()] = strategy

    def get(self, key):
        return self.store.get(key)
