from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import PasswordResetToken
from .serializers import PasswordResetSerializer
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from api.user.models import CustomUser
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
import random
from django.conf import settings

admin_email = getattr(settings, 'MY_ADMIN_EMAIL_ADDRESS',
                      settings.ADMIN_EMAIL_ADDRESS)


def generate_token(length=32):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(32)]) for _ in range(length))


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    queryset = PasswordResetToken.objects.all()

    def post(self, request, token=None):

        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            if token:
                user = get_object_or_404(
                    get_user_model(), passwordresettoken__token=token)
                token_obj = PasswordResetToken.objects.get(user=user)
                expiration_time = token_obj.created_at + \
                    timezone.timedelta(hours=1)

                if timezone.now() <= expiration_time:
                    new_password = serializer.validated_data['new_password']
                    user.set_password(new_password)
                    user.save()

                    # Optional: Invalidate the used reset token
                    token_obj.delete()

                    return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Password reset link has expired.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                email = serializer.validated_data['email']
                user = CustomUser.objects.filter(email=email).first()

                if user:
                    token = generate_token()
                    try:
                        old_token = PasswordResetToken.objects.get(user=user)
                        old_token.delete()

                    except PasswordResetToken.DoesNotExist:
                        pass  # No old token to delete

                    # Create a new token
                    new_token = PasswordResetToken.objects.create(
                        user=user, token=get_random_string(length=32), created_at=timezone.now())
                    # Send reset email
                    reset_link = f'http://localhost:3000/set-new-password/{new_token.token}'

                    to_email = email
                    displayName = user.displayName
                    subject = 'Reset Password Request'
                    recipient_list = [to_email]
                    message = ''
                    html_message = render_to_string('reset_password_template.html', {
                        'recipient_name': displayName, 'contact_email': admin_email, 'reset_link': reset_link})
                    email = EmailMessage(
                        subject,
                        message,
                        admin_email,
                        recipient_list,
                    )
                    email.content_subtype = 'html'  # Set the content type to HTML
                    email.body = html_message  # Set the HTML content
                    email.send()

                    return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
