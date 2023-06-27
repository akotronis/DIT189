# So that we can do from schemas import ... instead of from schemas.user import ...

from .divorce import DivorceInputSchema, DivorceNoMarriageSchema, DivorceSchema
from .marriage import MarriageInputSchema, MarriageSchema, MarriageUserDivorceSchema
from .user import UserInputSchema, UserSchema