from rest_framework.exceptions import ValidationError

def validate_pk(pk):
    try:
        pk = int(pk)
        if pk <= 0:
            raise ValidationError("Invalid employee ID")
        return pk
    except ValueError:
        raise ValidationError("Invalid employee ID")