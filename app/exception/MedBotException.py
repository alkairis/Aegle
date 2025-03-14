class MedBotException(Exception):
    def __init__(self, status_code, status_message, *args):
        self.status_code = status_code
        self.status_message = status_message
        super().__init__(*args)

    def __str__(self):
        return f"Exception(status_code={self.status_code}, status_message={self.status_message})"