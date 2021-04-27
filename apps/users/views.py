from django.contrib.sessions.models import Session

from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.models import User
from apps.users.api.serializers import UserTokenSerializer

class UserToken(APIView):
    """View for refresh user token

    """
    def get(self,request,*args, **kwargs):
        """get token

        Args:
            request (username)

        Returns:
            token: Renewed user token 
        """
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user = UserTokenSerializer().Meta.model.objects.filter(username = username).first()
            )
            return Response({
                'token':user_token.key
            })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas'
            }, status = status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):

        # serializer already defined in ObtainauthToken, called AuthTokenSererializer
        login_serializer = self.serializer_class(data=request.data, context={'request': request})

        if login_serializer.is_valid():
            
            user = login_serializer.validated_data['user']
            
            if user.is_active: 
                #get_or_create(ORM django) returns token,boolean
                token,created = Token.objects.get_or_create(user = user)
                #sent user serialzer
                user_serializer = UserTokenSerializer(user)

                if created:
                    #created token  
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso.'
                    },status = status.HTTP_201_CREATED)

                else:
                    """
                    # Process to close existing session and generate new token If the user is logged again elsewhere
                    # all sessions with expiration date greater or equal than right now
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    
                    if all_sessions.exists():
                        # for each session existent
                        for session in all_sessions:
                            # get_decoded() to get the session dictionary.
                            # This is necessary because the dictionary is stored in an encoded format
                            session_data = session.get_decoded()

                            #session with this user
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()

                    # token already created
                    token.delete()
                    # generate new token
                    token = Token.objects.create(user = user)

                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso.'
                    },status = status.HTTP_201_CREATED)
                    """

                    # Deny login again and delete token(for security if someone has obtained the token) to logout user
                    token.delete()
                    return Response({
                        'error': 'Ya se ha iniciado sesión con este usuario.'
                        }, status = status.HTTP_409_CONFLICT)

            else:
                #non active user
                return Response({'message': 'Este usuario no puede iniciar sesion'}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            #user invalid
            return Response({'error': 'Nombre de usuario y/o contraseña incorrectos.'},status = status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Hola desde response'}, status=status.HTTP_200_OK)

class Logout(APIView):

    def post(self,request,*args, **kwargs):
        try:

            token = Token.objects.filter(key = request.GET.get('token')).first()

            if token:
                user = token.user
                # Process to close existing session and generate new token If the user is logged again elsewhere
                # all sessions with expiration date greater or equal than right now
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                
                if all_sessions.exists():
                    # for each session existent
                    for session in all_sessions:
                        # get_decoded() to get the session dictionary.
                        # This is necessary because the dictionary is stored in an encoded format
                        session_data = session.get_decoded()

                        #session with this user
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()

                session_message = 'Sesiones de usuario elminadas'
                token_message = 'Token eliminado.'

                return Response({'session_message':session_message,'token_message':token_message},
                                    status = status.HTTP_200_OK)
            return Response({'error':'No se ha encontrado un usuario con estas credenciales.'},
                            status = status.HTTP_400_BAD_REQUEST)
        except:
            
            return Response({'error': 'No se ha encontrado token en la petición.'},
                                status = status.HTTP_409_CONFLICT)