from rest_framework import viewsets, generics, permissions, response, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re
from rest_framework.authtoken.models import Token
import secrets
import string
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

admin_email = getattr(settings, 'MY_ADMIN_EMAIL_ADDRESS',
                      settings.ADMIN_EMAIL_ADDRESS)


def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))


@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameters only'})

    username = request.POST.get('email')
    password = request.POST.get('password')

    # Validation part
    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error': 'Enter a valid email address'})

    if len(password) < 5:
        return JsonResponse({'error': 'Password needs to be at least 5 characters long'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            user_dict = UserModel.objects.filter(
                email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                # Login again regardless of previous session token
                s_token = generate_session_token()
                # Create or retrieve the token for the user
                token, created = Token.objects.get_or_create(user=user)
                user.session_token = s_token
                user.save()
                login(request, user)
                return JsonResponse({'success': 'Login Successful', 'token': str(token), 'user': user_dict})
                # return JsonResponse({'error': 'Previous session exists!'})
            s_token = generate_session_token()
            # Create or retrieve the token for the user
            token, created = Token.objects.get_or_create(user=user)
            user.session_token = s_token
            user.save()
            login(request, user)
            return JsonResponse({'success': 'Login Successful', 'token': str(token), 'user': user_dict})
        else:
            return JsonResponse({'error': 'Invalid password'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email Address'})


def signout(request, id):
    logout(request)

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error', 'Invalid user'})
    return JsonResponse({'success': 'Logout successfully'})


def generate_referral_code(length=8):
    characters = string.ascii_letters + string.digits
    referral_code = ''.join(secrets.choice(characters) for _ in range(length))
    return referral_code.upper()
    # return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(6)]) for _ in range(length))


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        if self.action == 'create':
            return []
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        data = request.data
        email = request.data.get('email', None)
        displayName = request.data.get('displayName', None)
        data['referralCode'] = generate_referral_code()

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': True, 'message': "This email address is already in use.", "status": status.HTTP_400_BAD_REQUEST})

        if CustomUser.objects.filter(displayName=displayName).exists():
            return JsonResponse({'success': False, 'error': True, 'message': "This username is already in use.", "status": status.HTTP_400_BAD_REQUEST})

        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            # user = self.perform_create(serializer)
            user = serializer.save()
            user.generate_verification_token()
            to_email = email
            subject = 'Welcome to iPadel'
            recipient_list = [to_email]
            message = ''
            html_message = render_to_string('welcome_email_template.html', {
                'recipient_name': displayName, 'contact_email': admin_email, 'verification_link': self.get_verification_url(user)})
            email = EmailMessage(
                subject,
                message,
                admin_email,
                recipient_list,
            )
            email.content_subtype = 'html'
            email.body = html_message
            email.send()
            return JsonResponse({'success': True, 'error': False, 'message': 'Sign-up successful! Kindly log-in.',  "status": status.HTTP_200_OK})
        return JsonResponse({'success': False, 'error': True, 'message': "Sign-up failed. Please try again.", "status": status.HTTP_400_BAD_REQUEST})

    def get_verification_url(self, user):
        client_url = getattr(settings, 'CLIENT_URL', settings.CLIENT_SIDE_URL)
        return f'{client_url}/verify-email/{user.id}/{user.verification_token}/'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # Custom action to retrieve by get_user_by_username
    @action(detail=False, methods=['get'])
    def get_user_by_displayName(self, request):
        displayName = request.query_params.get('displayName', None)
        if displayName is not None:
            records = CustomUser.objects.filter(displayName=displayName)
            if (len(records) > 0):
                serializer = self.get_serializer(records, many=True)
                return JsonResponse({'success': True, 'error': False, 'message': 'Profile retrieved successfully', 'data': serializer.data, "status": status.HTTP_200_OK})
            return JsonResponse({'success': False, 'error': True, 'message': "Profile record not found", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})

        else:
            return JsonResponse({'success': False, 'error': True, 'message': "Profile name not found", "status": status.HTTP_400_BAD_REQUEST, 'data': {}})


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        print(user_id)
        user = get_object_or_404(get_user_model(), id=user_id)
        print(user)
        if not user.isVerified:
            user.isVerified = True
            user.save()
            return response.Response({'detail': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return response.Response({'detail': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        client_url = getattr(settings, 'CLIENT_URL', settings.CLIENT_SIDE_URL)

        id = request.data['id']
        verification_token = request.data['verification_token']
        url = f'{client_url}/verify-email/{id}/{verification_token}/'

        user = request.user

        if not user.isVerified or not user.is_verification_token_valid():
            user.resend_verification_email()
            user.save()
            to_email = user
            subject = 'Welcome to iPadel'
            recipient_list = [to_email]
            message = ''
            html_message = render_to_string('resend_email_template.html', {
                'recipient_name': user, 'contact_email': admin_email, 'verification_link': url})
            email = EmailMessage(
                subject,
                message,
                admin_email,
                recipient_list,
            )
            email.content_subtype = 'html'
            email.body = html_message
            email.send()
            return response.Response({'detail': 'Verification email resent successfully.'}, status=status.HTTP_200_OK)
        else:
            return response.Response({'detail': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
