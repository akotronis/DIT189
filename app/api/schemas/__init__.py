# So that we can do from schemas import ... instead of from schemas.user import ...

from .divorce import DivorceCreateSchema, DivorceInputSchema, DivorceInputUpdateSchema, DivorceNoMarriageSchema, DivorceSchema
from .marriage import MarriageInputSchema, MarriageSchema, MarriageUserDivorceSchema
from .refresh import RefreshInputSchema
from .user import KeycloakUserInputSchema, KeycloakUserOutputSchema, UserInputSchema, UserSchema
from .user_divorce import UserConfirmationsSchema