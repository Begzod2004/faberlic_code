import uuid

from rest_framework.exceptions import ValidationError


def generate_unique_filename(instance, filename):
    extension = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    return f"images/{unique_filename}"


class SymbolValidationMixin:
    def validate_symbols(self, data):
        fields_to_check = [
            "title_en",
            "title_uz",
            "title_ru",
            "sub_title_en",
            "sub_title_uz",
            "sub_title_ru",
        ]

        for field in fields_to_check:
            if field in data and any(char in data[field] for char in "\<>&"):
                raise ValidationError(f"Field '{field}' contains disallowed symbols.")

    def validate(self, data):
        self.validate_symbols(data)
        return data
