from datetime import date, datetime
from decimal import Decimal


class SerializerMixin:
    def to_dict(self) -> dict:
        data = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)

            data[column.name] = value

        return data
