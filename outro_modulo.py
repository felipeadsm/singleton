from modo_generico import singleton


@singleton
class Singleton:

    def __init__(self):
        self.some_attribute = None
