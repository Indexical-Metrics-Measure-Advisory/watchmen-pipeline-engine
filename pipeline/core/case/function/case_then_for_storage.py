from typing import List

from pipeline.config.config import settings
from pipeline.core.case.model.parameter import Parameter

MYSQL = "mysql"
MONGO = "mongo"
ORACLE = "oracle"


def find_case_then_template():
    if settings.STORAGE_ENGINE == MONGO:
        from pipeline.core.case.function import case_then_for_mongo
        return case_then_for_mongo
    elif settings.STORAGE_ENGINE == MYSQL:
        from pipeline.core.case.function import case_then_for_oracle
        return case_then_for_oracle
    elif settings.STORAGE_ENGINE == ORACLE:
        from pipeline.core.case.function import case_then_for_oracle
        return case_then_for_oracle


case_then_template = find_case_then_template()


def parse_storage_case_then(parameters_: List[Parameter]):
    return case_then_template.parse_storage_case_then(parameters_)
