import logging
import operator
from decimal import Decimal

log = logging.getLogger("app." + __name__)


def do_not_in_with_value_type_check(left, right):
    if left is None or right is None or right == "":
        return True

    if (isinstance(left, str) or isinstance(left, int) or isinstance(left, Decimal)) and isinstance(right, str):
        value_list = right.split(',')
        return not operator.contains(value_list, str(left))

    if (isinstance(left, str) or isinstance(left, int) or isinstance(left, Decimal)) and isinstance(right, list):
        for value in right:
            if operator.eq(str(left), str(value)):
                return False

    log.info("operator not in, the left \"{0}\" is not in the right \"{1}\"".format(left, right))
    return True
