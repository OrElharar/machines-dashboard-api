class CustomException(Exception):
    def __init__(self, message="A custom exception occurred", status_code=500):
        super().__init__(message)
        self.status_code = status_code
