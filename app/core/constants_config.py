from app.core.enums import OperatorEnum

ALL_FIELDS = "__all__"

FIELDS_LOOKUPS = {
    OperatorEnum.EQ.value: "==",
    OperatorEnum.NE.value: "!=",
    OperatorEnum.GT.value: ">",
    OperatorEnum.LT.value: "<",
    OperatorEnum.GTE.value: ">=",
    OperatorEnum.LTE.value: "<=",
    OperatorEnum.IS_NULL.value: "is_null",
    OperatorEnum.IS_NOT_NULL.value: "is_not_null",
    OperatorEnum.LIKE.value: "like",
    OperatorEnum.ILIKE.value: "ilike",
    OperatorEnum.NOT_LIKE.value: "not_ilike",
}
