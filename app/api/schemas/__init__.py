# So that we can do from schemas import ... instead of from schemas.user import ...

from .divorce import DivorceSchema
from .marriage import MarriageSchema, MarriageUserDivorceSchema
from .user import UserInputSchema, UserSchema