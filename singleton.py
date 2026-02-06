class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            print("Logger Initialized")
        return cls._instance

    def log(self, message):
        print(f"[LOG]: {message}")