from rest_framework.authentication import get_authorization_header
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from apps.users.authentications import ExpiringTokenAuthentication


class Authentication(object):
    """Authentication mixin

    """
    user = None
    user_token_expired = False
    
    def get_user(self,request):
        """[summary]

        Args:
            request ([type]): [description]
        
        Method used:
            get_authorization_header():Return request's 'Authorization:' header, as a bytestring.
                Hide some test client ickyness where the header can be unicode.
            
        Returns:
            [type]: [description]
        """
        token = get_authorization_header(request).split()
        if token:
            try:
                # eg token = [b'Token', b'c1d377ce440e6569db446f9954a32a2218697474'
                token = token[1].decode()   
            except:
                return None 

            #token_expired = ExpiringTokenAuthentication() --> its the same
            user,token,message,self.user_token_expired = ExpiringTokenAuthentication().authentication_credentials(token)
            if user != None and token != None:
                self.user = user
                return user
            return message
        return None

    def dispatch(self, request, *args, **kwargs):
        """dispatch accepts a request argument plus arguments, and returns a HTTP response.

        Args:
            request (str): user - model.__str__()
        """
        user = self.get_user(request)
        # found token in request
        if user is not None:
            
            if type(user) == str:
                response =  Response({'error': user,'expired':self.user_token_expired},
                                        status = status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                return response

            if not self.user_token_expired:    
                return super().dispatch(request, *args, **kwargs)

        response = Response({'error':'No se han enviado las credenciales.','expired':self.user_token_expired},
                                status = status.HTTP_400_BAD_REQUEST)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response
    