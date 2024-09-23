from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class DynamicModelSchema(SQLAlchemyAutoSchema):
    """Schema para processar múltiplos modelos de forma dinâmica"""

    def __init__(self, nested_fields=None, *args, **kwargs):
        super().__init__(**kwargs)

        if nested_fields:
            for field_name, model in nested_fields.items():
                schema = model.get_schema()
                setattr(self, field_name, fields.Nested(schema))

    def dump(self, data, **kwargs):
        if isinstance(data, tuple) and len(data) > 1:
            primary_instance = data[0]

            result = super().dump(primary_instance)

            nested_field_names = [
                key
                for key, value in self.fields.items()
                if isinstance(value, fields.Nested)
            ]

            for idx, related_instance in enumerate(data[1:], start=1):
                if idx <= len(nested_field_names):
                    field_name = nested_field_names[idx - 1]

                    nested_schema_instance = self.fields[field_name].schema

                    result[field_name] = nested_schema_instance.dump(related_instance)

            return result

        return super().dump(data, **kwargs)
