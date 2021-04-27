from datetime import timedelta, timezone

from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    """Expiration authentication of the Token

    Args:
        TokenAuthentication (BaseAuthentication): Simple token based authentication.
            Clients should authenticate by passing the token key in the "Authorization"
            HTTP header, prepended with the string "Token ".  For example:
            Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    
    """
    # to send to the frontend
    expired = False

    def expires_in(self,token):
        """Calculate the expiration time of the Token

        """
        # time elapsed = current date - date created token
        time_elapsed = timezone.now() - token.created
        # 10 sec - time_elapsed, must be negative usually
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired(self,token):
        """Expiration token

        Returns:
            Boolean: True if left_time is negative
        """
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expire_handler(self,token):
        """Expired token
        
        """
        is_expire = self.is_token_expired(token)

        if is_expire:
            self.expired = True
            # save user of expired token
            user = token.user
            token.delete()
            # create new token
            token = self.get_model().objects.create(user = user)

        return is_expire,token

    def authentication_credentials(self,key):
        """Authentication of credentials

        Args:
            key (token): token request
        """
        message,token,user = None,None,None
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
            user = token.user

        except self.get_model().DoesNotExist:
            message = 'Token inválido.'
            self.expired = True
        
        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no activo o eliminado.'

            is_expired = self.token_expire_handler(token)

            if is_expired:
                message = 'Su token ha expirado'

        return(user,token,message,self.expired)