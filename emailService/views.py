import ast
from django.core.mail import EmailMultiAlternatives, get_connection
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

def send_mail_func(subject, recipient_list, from_email, html_body, host_password, attachments=None):
    text_content = strip_tags(html_body)
    
    # Create the dynamic connection
    connection = get_connection(
        username=from_email,
        password=host_password,
        fail_silently=False
    )

    msg = EmailMultiAlternatives(
        subject, 
        text_content, 
        from_email, 
        to=recipient_list, 
        bcc=recipient_list,
        connection=connection
    )
    
    msg.attach_alternative(html_body, "text/html")

    # <--- NEW: Handle Attachments --->
    if attachments:
        for file in attachments:
            # Django's UploadedFile object has .name, .read(), and .content_type
            msg.attach(file.name, file.read(), file.content_type)

    msg.send()

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser]) # <--- Enable file uploads
def trigger_mail(request):
    try:
        subject = request.data.get("subject")
        recipient_data = request.data.get("toEmails")
        from_email = request.data.get("fromEmail")
        host_password = request.data.get("hostPassword") 
        
        # <--- NEW: Handle Template Logic --->
        # 1. Check if an HTML file was uploaded as 'emailTemplate'
        template_file = request.FILES.get('emailTemplate')
        
        if template_file:
            # Read the file and decode bytes to string
            html_body = template_file.read().decode('utf-8')
        else:
            # 2. Fallback to the string body
            html_body = request.data.get("emailBody")

        # <--- NEW: Capture Attachments --->
        # Expects frontend to append multiple files to key 'attachments'
        attachment_files = request.FILES.getlist('attachments')

        # Validation
        if not from_email or not host_password:
            return JsonResponse({"message": "fromEmail and hostPassword are required"}, status=400)

        # Recipient List Parsing
        recipient_list = []
        if isinstance(recipient_data, list):
            recipient_list = recipient_data
        elif isinstance(recipient_data, str):
            try:
                recipient_list = ast.literal_eval(recipient_data)
            except:
                clean_str = recipient_data.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                recipient_list = [email.strip() for email in clean_str.split(",") if email.strip()]

        if not recipient_list or not isinstance(recipient_list, list):
             return JsonResponse({"message": "Invalid email list"}, status=400)

        # Send
        send_mail_func(
            subject, 
            recipient_list, 
            from_email, 
            html_body, 
            host_password, 
            attachments=attachment_files # Pass files to function
        )
        
        return JsonResponse({"message": f"Email sent with {len(attachment_files)} attachments"}, status=200)

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": str(e)}, status=500)