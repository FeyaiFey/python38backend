from pydantic import EmailStr, ValidationError

def validate_email(email: str) -> bool:
    try:
        EmailStr._validate(email)
        return True
    except:
        return False