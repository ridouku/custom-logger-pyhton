import unittest
from logger.Logger import CustomLogger


def this_fails():
    1 / 0


class TestCustomLogger(unittest.TestCase):
    def setUp(self):
        self.logger = CustomLogger()

    def test_log_info(self):
        """
        it test log info
        """
        self.assertEqual(None, self.logger.info("test log info",
                                                {"secret_key": "ASDASF-asdaaSDASD===",
                                                 "cardNumber": "1312314123",
                                                 "bin": "453634654",
                                                 "card":
                                                     {"number": "4242424242424242",
                                                      "bin": "453634654",
                                                      "expiryYear": "23",
                                                      "expiryMonth": "12",
                                                      "cvv": "123"}}))

    def test_log_info_with_empty_metadata(self):
        """
        it test log info with empty metadata
        """
        self.assertEqual(None, self.logger.info("test log information", 13123))

    def test_log_warn(self):
        """
        it test log warn
        """
        self.assertEqual(None, self.logger.warning("test log warning", 2314))

    def test_log_error(self):
        """
        it test log error
        """
        self.assertEqual(None, self.logger.error("test log error", "23"))

    def test_log_info_with_exception_param(self):
        """
        it test log info with exception param
        """
        try:
            this_fails()
        except ZeroDivisionError as err:
            self.assertEqual(None, self.logger.info(err, {}))


if __name__ == '__main__':
    unittest.main()
