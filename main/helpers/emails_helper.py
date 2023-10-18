import os
from dataclasses import dataclass

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth


@dataclass
class EmailHandler:
    email: str

    def signup_otp_confirmation(self, first_name, year, otp):
        """
        SEND CV REVIEW PAYMENT CONFIRMATION EMAIL
        """

        html = """\
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Verification</title>
    <style>
        /* Reset styles */
        body, p {
            margin: 0;
            padding: 0;
        }
        
        /* Container */
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Header */
        .header {
            background-color: #dd3051;
            color: #ffffff;
            text-align: center;
            padding: 20px 0;
        }
        
        /* Content */
        .content {
            background-color: #ffffff;
            padding: 20px;
        }
        
        /* Verification Code */
        .verification-code {
            font-size: 24px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Call to Action Button */
        .cta-button {
            text-align: center;
            margin-top: 20px;
        }
        
        .cta-button a {
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <table class="container" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="header">
                            <h1>Account Verification</h1>
                        </td>
                    </tr>
                    <tr>
                        <td class="content">
                            <p>Hello $first_name,</p>
                            <p>Thank you for creating an account with us. To verify your account, please use the following verification code:</p>
                            <p class="verification-code">$otp</p>
                            <p>If you did not create an account with us, please disregard this email.</p>
                        </td>
                    </tr>
                    <tr>
                        <td class="footer">
                            <p>&copy; $year Tunga TIA. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>~
</body>
</html>


        """

        html = html.replace("$first_name", first_name)
        html = html.replace("$otp", str(otp))

        html = html.replace("$year", str(year))

        response = requests.post(
            "https://api.mailgun.net/v3/mg.getlinked.ai/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": "Tunga TIA <postmaster@getlinked.ai>",
                "to": f"{self.email}",
                "subject": "Account Verification",
                "html": html,
            },
        )

        # print(response.text)
        return response.text

    def account_reset_request(self, first_name, year, otp):
        """
        SEND ACCOUNT RESET REQUEST EMAIL
        """

        html = """\

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Verification</title>
    <style>
        /* Reset styles */
        body, p {
            margin: 0;
            padding: 0;
        }
        
        /* Container */
        .container {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Header */
        .header {
            background-color: #dd3051;
            color: #ffffff;
            text-align: center;
            padding: 20px 0;
        }
        
        /* Content */
        .content {
            background-color: #ffffff;
            padding: 20px;
        }
        
        /* Verification Code */
        .verification-code {
            font-size: 24px;
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Call to Action Button */
        .cta-button {
            text-align: center;
            margin-top: 20px;
        }
        
        .cta-button a {
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <table class="container" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="header">
                            <h1>Account Reset</h1>
                        </td>
                    </tr>
                    <tr>
                        <td class="content">
                            <p>Hello $first_name,</p>
                            <p>We received a request to reset your password. To reset your password, please use the following verification code:</p>
                            <p class="verification-code">$otp</p>
                            <p>If you didn't request a password reset, you can safely ignore this email.</p>
                        </td>
                    </tr>
                    <tr>
                        <td class="footer">
                            <p>&copy; $year Tunga TIA. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>


        """

        html = html.replace("$first_name", first_name)
        html = html.replace("$otp", str(otp))

        html = html.replace("$year", str(year))

        response = requests.post(
            "https://api.mailgun.net/v3/mg.getlinked.ai/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": "Tunga TIA <postmaster@getlinked.ai>",
                "to": f"{self.email}",
                "subject": "Account Reset",
                "html": html,
            },
        )

    def send_file_report_ro_user(self, file_name, first_name, year):
        """
        SEND FILE REPORT TO USER
        """

        html = """\
                <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DIARY NOTE FILE</title>
        <style>
            /* Reset styles */
            body, p {
                margin: 0;
                padding: 0;
            }
            
            /* Container */
            .container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
            }
            
            /* Header */
            .header {
                background-color: #dd3051;
                color: #ffffff;
                text-align: center;
                padding: 20px 0;
            }
            
            /* Content */
            .content {
                background-color: #ffffff;
                padding: 20px;
            }
            
            /* Verification Code */
            .verification-code {
                font-size: 24px;
                text-align: center;
                margin-bottom: 20px;
            }
            
            /* Call to Action Button */
            .cta-button {
                text-align: center;
                margin-top: 20px;
            }
            
            .cta-button a {
                background-color: #007bff;
                color: #ffffff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <table class="container" cellpadding="0" cellspacing="0">
            <tr>
                <td>
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td class="header">
                                <h1>Diary Note file</h1>
                            </td>
                        </tr>
                        <tr>
                            <td class="content">
                                <p>Hello $first_name,</p>
                                <p>Your diary note file is ready, please check the attachement of this email, you'll see the file</p>
                            </td>
                        </tr>
                        <tr>
                            <td class="footer">
                                <p>&copy; $year Tunga TIA. All rights reserved.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
        """

        html = html.replace("$first_name", first_name)
        html = html.replace("$year", str(year))

        with open(file_name, "rb") as file:
            files = {"attachment": (file_name.split("/")[-1], file)}

            response = requests.post(
                "https://api.mailgun.net/v3/mg.getlinked.ai/messages",
                auth=HTTPBasicAuth("api", settings.MAILGUN_API_KEY),
                files=files,
                data={
                    "from": "Tunga TIA <postmaster@getlinked.ai>",
                    "to": f"{self.email}",
                    "subject": "Diary Note Download",
                    "html": html,
                },
            )

        try:
            os.remove(file_name)
        except FileNotFoundError:
            pass

    def send_reminder(self, first_name, year, reminder_message, note_title):
        """
        SEND REMINDER TO USER
        """

        html = """\
           <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reminder</title>
        <style>
            /* Reset styles */
            body, p {
                margin: 0;
                padding: 0;
            }
            
            /* Container */
            .container {
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
            }
            
            /* Header */
            .header {
                background-color: #dd3051;
                color: #ffffff;
                text-align: center;
                padding: 20px 0;
            }
            
            /* Content */
            .content {
                background-color: #ffffff;
                padding: 20px;
            }
            
            /* Verification Code */
            .verification-code {
                font-size: 24px;
                text-align: center;
                margin-bottom: 20px;
            }
            
            /* Call to Action Button */
            .cta-button {
                text-align: center;
                margin-top: 20px;
            }
            
            .cta-button a {
                background-color: #007bff;
                color: #ffffff;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <table class="container" cellpadding="0" cellspacing="0">
            <tr>
                <td>
                    <table width="100%" cellpadding="0" cellspacing="0">
                        <tr>
                            <td class="header">
                                <h1>Reminder - $note_title</h1>
                            </td>
                        </tr>
                        <tr>
                            <td class="content">
                                <p>Hello $first_name,</p>
                                <p>$reminder_message</p>
                            </td>
                        </tr>
                        <tr>
                            <td class="footer">
                                <p>&copy; $year Tunga TIA. All rights reserved.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
"""
        html = html.replace("$first_name", first_name)
        html = html.replace("$reminder_message", str(reminder_message))
        html = html.replace("$note_title", str(note_title))

        html = html.replace("$year", str(year))

        response = requests.post(
            "https://api.mailgun.net/v3/mg.getlinked.ai/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": "Tunga TIA <postmaster@getlinked.ai>",
                "to": f"{self.email}",
                "subject": "Reminder",
                "html": html,
            },
        )
