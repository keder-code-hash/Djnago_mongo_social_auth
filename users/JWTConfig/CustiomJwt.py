from users.models.JwtTokwnModels import OutstandingToken,BlacklistedToken

from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import datetime_from_epoch
 

class CustomRefreshToken(RefreshToken): 

    def blacklist(self): 
        jti = self.payload[api_settings.JTI_CLAIM]
        exp = self.payload["exp"] 

        try : 
        # Ensure outstanding token exists with given jti
            token = OutstandingToken.objects.get(
                jti__iexact = jti, token = str(self), expires_at =  datetime_from_epoch(exp) 
            )
            print("TOken Str: ")
            print(str(token._id))

            return BlacklistedToken.objects.get_or_create(token = token._id)
        except:
            return InvalidToken()

    @classmethod
    def for_user(cls, user): 
        
        token = super().for_user(user)

        jti = token[api_settings.JTI_CLAIM]
        exp = token["exp"]

        OutstandingToken.objects.create(
            user_id=user._id,
            jti=jti,
            token=str(token),
            created_at=token.current_time,
            expires_at=datetime_from_epoch(exp),
        )

        return token
    