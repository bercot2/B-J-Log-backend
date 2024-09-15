from enum import Enum


class OperatorEnum(Enum):
    IS_NULL = 'is_null'
    IS_NOT_NULL = 'is_not_null'
    EQ = 'eq'
    NE = 'ne'
    GT = 'gt'
    LT = 'lt'
    GTE = 'gte'
    LTE = 'lte'
    LIKE = 'like'
    ILIKE = 'ilike'
    NOT_LIKE = 'not_ilike'