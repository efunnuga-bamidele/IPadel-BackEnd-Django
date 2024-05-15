# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from .serializers import EmailSerializer
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from django.conf import settings

admin_email = getattr(settings, 'MY_ADMIN_EMAIL_ADDRESS',
                      settings.ADMIN_EMAIL_ADDRESS)


class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            displayName = serializer.validated_data['displayName']
            subject = serializer.validated_data['subject']
            # message = serializer.validated_data['message']
            recipient_list = [to_email]
            message = ''
            html_message = render_to_string('welcome_email_template.html', {
                'recipient_name': displayName, 'contact_email': admin_email})
            email = EmailMessage(
                subject,
                message,
                admin_email,
                recipient_list,
            )
            email.content_subtype = 'html'  # Set the content type to HTML
            email.body = html_message  # Set the HTML content
            email.send()

            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
