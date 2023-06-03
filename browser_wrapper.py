class Browser:
    def __init__(self, id, driver):
        self.id = id
        self.driver = driver
        self.is_busy = False
