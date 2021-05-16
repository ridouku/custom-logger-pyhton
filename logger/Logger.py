from definitions.Logger import MaskTargetsKeys
from typing import Union
from jsonpath_ng import parse
import json
import pydash
import logging


class CustomLogger:
    def __init__(self) -> None:
        CustomLogger.__set_masked_keys(self)
        logging.basicConfig(format='[%(levelname)s] : %(message)s', level=logging.INFO)
        super().__init__()

    def info(self, message: Union[str, Exception], metadata: dict = None) -> None:
        logging.info(CustomLogger.__message(self,
                                            message,
                                            metadata))

    def warning(self, message: Union[str, Exception], metadata: dict = None) -> None:
        logging.warning(CustomLogger.__message(self,
                                               message,
                                               metadata))

    def error(self, message: Union[str, Exception], metadata: dict = None) -> None:
        logging.error(CustomLogger.__message(self,
                                             message,
                                             metadata))

    def __set_masked_keys(self) -> None:
        self.__mask_targets = []
        credit_card_key = MaskTargetsKeys.CREDIT_CARD.value
        cvv_key = MaskTargetsKeys.CVV.value
        exp_date_key = MaskTargetsKeys.EXP_DATE.value
        bin_key = MaskTargetsKeys.BIN.value
        secret_key = MaskTargetsKeys.SECRET_KEY.value
        self.__mask_targets.append(MaskTargets(credit_card_key, "$..card.number"))
        self.__mask_targets.append(MaskTargets(credit_card_key, "$..cardNumber"))
        self.__mask_targets.append(MaskTargets(cvv_key, "$..cvv"))
        self.__mask_targets.append(MaskTargets(exp_date_key, "$..expiryMonth"))
        self.__mask_targets.append(MaskTargets(exp_date_key, "$..expiryYear"))
        self.__mask_targets.append(MaskTargets(bin_key, "$..bin"))
        self.__mask_targets.append(MaskTargets(secret_key, "$..password"))
        self.__mask_targets.append(MaskTargets(secret_key, "$..secret_key"))

        return

    def __mask_credit_data(self, data: str) -> str:
        return data[:6] + 'X' * 6 + data[-4:]

    def __mask_bin_data(self, data: str) -> str:
        return data[:6] + 'X' * (len(data) - 6)

    def __mask_secret_data(self, data: str) -> str:
        return data[:2] + '*********' + (data[-1:])

    def __clear_sensitive_data(self, metadata: dict) -> dict:

        for item in self.__mask_targets:
            json_path_expression = parse(item.expression)
            json_path_expression.find(metadata)
            matches = [str(match.full_path) for match
                       in json_path_expression.find(metadata)]
            for match in matches:
                target_value = pydash.get(metadata, match, default="")

                if item.target == MaskTargetsKeys.CREDIT_CARD.value:
                    mask_data = CustomLogger.__mask_credit_data(self, target_value)
                    pydash.set_(metadata, match, mask_data)
                if item.target == MaskTargetsKeys.BIN.value:
                    mask_data = CustomLogger.__mask_bin_data(self, target_value)
                    pydash.set_(metadata, match, mask_data)
                if item.target == MaskTargetsKeys.EXP_DATE.value:
                    pydash.set_(metadata, match, "XX")
                if item.target == MaskTargetsKeys.CVV.value:
                    pydash.set_(metadata, match, "XXX")
                if item.target == MaskTargetsKeys.SECRET_KEY.value:
                    mask_data = CustomLogger.__mask_secret_data(self, target_value)
                    pydash.set_(metadata, match, mask_data)

        return metadata

    def __message(self,
                  message: Union[str,
                                 Exception],
                  metadata: dict = None) -> str:
        msg: str = str(message)
        if isinstance(metadata, dict):
            clone_data = pydash.clone_deep(metadata)
            masked_data = CustomLogger.__clear_sensitive_data(self, clone_data)
            sensitive_data = json.dumps(masked_data, indent=1)
            return msg + " " + sensitive_data

        return msg + " " + str(metadata)


class MaskTargets:

    def __init__(self, target: str, expression: str):
        self.target = target
        self.expression = expression
        pass
