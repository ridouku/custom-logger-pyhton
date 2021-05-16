from logger.Logger import CustomLogger


class HelloLogger:
    def __init__(self) -> None:
        self.logger = CustomLogger()
        super().__init__()

    def hello_logger(self) -> None:
        test_data = {
            "secret_key": "ASDASF-asdaaSDASD===",
            "cardNumber": "1312314123",
            "password": "password1234",
            "bin": "453634654",
            "card":
                {"number": "4242424242424242",
                 "bin": "453634654",
                 "expiryYear": "23",
                 "expiryMonth": "12",
                 "cvv": "123"}
        }
        self.logger.info("Test Data", test_data)
