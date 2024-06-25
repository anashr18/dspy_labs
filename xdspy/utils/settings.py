from xdspy.utils.utils import dotdict


class Settings(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.stack = []

            config = dotdict()
            cls._instance.__append(config)

        return cls._instance

    @property
    def config(self):
        return self.stack[-1]

    def __getattr__(self, name):
        if hasattr(self.config, name):
            return getattr(self.config, name)

        if name in self.config:
            return self.config[name]

        super().__getattr__(name)

    def __append(self, config):
        self.stack.append(config)

    def __pop(self):
        return self.stack.pop()

    def configure(self, inherit_config=True, **kwargs):
        if inherit_config:
            config = {**self.config, **kwargs}
        self.__append(config)

    def __repr__(self) -> str:
        return repr(self.config)


settings = Settings()
