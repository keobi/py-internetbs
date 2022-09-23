from marshmallow import fields


__all__ = [
    "SpecialBoolField", "YesNoBoolField",
]


class SpecialBoolField(fields.Field):
    def _deserialize(self, value, attr, obj, **kwargs):
        value = value.lower()

        true_value = kwargs.get("true_value")

        if not isinstance(true_value, list):
            true_value = [true_value]

        return value in true_value

    def _serialize(self, value, attr, obj, **kwargs):
        true_value = kwargs.get("true_value")
        false_value = kwargs.get("false_value")

        if isinstance(true_value, list):
            true_value = true_value[0]

        if isinstance(false_value, list):
            false_value = false_value[0]

        value = true_value if value else false_value

        if kwargs.get("upper", False):
            value = value.upper()

        return value


class YesNoBoolField(fields.Field):
    def _deserialize(self, value, attr, obj, **kwargs):
        return value.lower() == "yes"

    def _serialize(self, value, attr, obj, **kwargs):
        value = "yes" if value else "no"

        if kwargs.get("upper", False):
            value = value.upper()

        return value
