import datetime
import decimal
import uuid


class BaseServiceModel:
    """
    Bazna klasa za sve Service Modele.
    - from_dict / from_row : mapira ulaz (JSON body ili SP red) u instancu modela
    - to_dict              : konvertuje model u dict spreman za JSON
    - to_sp_params         : dict za named parametre stored procedure (preskace None)
    """

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, BaseServiceModel):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [
                    v.to_dict() if isinstance(v, BaseServiceModel) else BaseServiceModel._serialize_value(v)
                    for v in value
                ]
            else:
                result[key] = BaseServiceModel._serialize_value(value)
        return result

    @staticmethod
    def _serialize_value(value):
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        if isinstance(value, decimal.Decimal):
            return float(value)
        if isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="ignore")
        return value

    @classmethod
    def from_row(cls, row):
        """Kreira instancu iz dict reda vracenog iz SP-a (case-insensitive mapping)."""
        if row is None:
            return None
        instance = cls()
        model_attrs = {k.lower(): k for k in instance.__dict__.keys()}
        for col_name, col_value in row.items():
            key = col_name.lower()
            if key in model_attrs:
                setattr(instance, model_attrs[key], col_value)
            else:
                setattr(instance, col_name, col_value)
        return instance

    @classmethod
    def from_rows(cls, rows):
        return [cls.from_row(r) for r in (rows or [])]

    @classmethod
    def from_dict(cls, data):
        """Kreira instancu iz JSON dict-a (case-insensitive mapping na model atribute)."""
        instance = cls()
        if not data:
            return instance
        model_attrs = {k.lower(): k for k in instance.__dict__.keys()}
        for key, value in data.items():
            lk = key.lower()
            if lk in model_attrs:
                setattr(instance, model_attrs[lk], value)
        return instance
