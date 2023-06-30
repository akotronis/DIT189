# So that we can do from schemas import ... instead of from schemas.user import ...

from .divorce import DivorceCreateSchema, DivorceInputSchema, DivorceInputUpdateSchema, DivorceNoMarriageSchema, DivorceSchema, DivorceUpdateSchema
from .marriage import MarriageInputSchema, MarriageSchema, MarriageUserDivorceSchema
from .user import UserInputSchema, UserSchema
from .user_divorce import UserConfirmationsSchema