import ast  # <--- 1. ADD THIS IMPORT AT THE VERY TOP
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view

def send_mail_func(subject, recipient_list, from_email, html_body):
    text_content = strip_tags(html_body)
    msg = EmailMultiAlternatives(
        subject, 
        text_content, 
        from_email, 
        to=[from_email], 
        bcc=recipient_list
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()

@api_view(['POST'])
def trigger_mail(request):
    try:
        subject = request.data.get("subject")
        recipient_data = request.data.get("toEmails")
        from_email = request.data.get("fromEmail") or settings.DEFAULT_FROM_EMAIL
        html_body = request.data.get("emailBody")

        # --- FIX START: Convert String to List ---
        recipient_list = []

        if isinstance(recipient_data, list):
            # It is already a list (Perfect scenario)
            recipient_list = recipient_data
        
        elif isinstance(recipient_data, str):
            # It is a string like "['email1', 'email2']"
            try:
                # ast.literal_eval safely converts a stringified Python list back to a list
                recipient_list = ast.literal_eval(recipient_data)
            except:
                # Fallback: manually strip brackets and quotes if ast fails
                clean_str = recipient_data.replace("[", "").replace("]", "").replace("'", "").replace('"', "")
                recipient_list = [email.strip() for email in clean_str.split(",") if email.strip()]
        # --- FIX END ---

        # Validate
        if not recipient_list or not isinstance(recipient_list, list):
             return JsonResponse({"message": "Invalid email list"}, status=400)

        # Send
        send_mail_func(subject, recipient_list, from_email, html_body)
        
        return JsonResponse({"message": f"Email sent to {len(recipient_list)} recipients"}, status=200)

    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)