import requests

# 1. API Endpoint (Replace with your actual Vercel URL)
url = "https://orconix-email-service.vercel.app/orconixemailservice/sendemail"  

# 2. Data Payload
payload = {
    'subject': "Your Account Has been Debited",
    
    # Note: The backend expects "toEmails" (plural) as a list string
    'toEmails': "['kubetkarpratham14@gmail.com','hatekaramay25@gmail.com']", 
    
    'fromEmail': "orconixindia@gmail.com",
    
    # Note: Backend expects "emailBody" (not htmlBody)
    'emailBody': "<h1>If you see this mail send a ScreenShot to Pratham</h1><p>This was a test email to check Django's SMTP Server</p>",

    # CRITICAL: You must provide the App Password for the 'fromEmail' account
    'hostPassword': "isxp fmco olwu gtnw" 
}

# 3. Optional: Send an attachment (Uncomment to test)
# files = [
#     ('attachments', ('invoice.pdf', open('path/to/invoice.pdf', 'rb'), 'application/pdf'))
# ]

try:
    # Sending as POST request
    # usage of 'data' automatically sets Content-Type to application/x-www-form-urlencoded
    # If sending files, use: requests.post(url, data=payload, files=files)
    response = requests.post(url, data=payload)

    # 4. Check Response
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print(f"Failed ({response.status_code}):", response.text)

except Exception as e:
    print("Error:", str(e))