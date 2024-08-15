import smtplib
import argparse
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
Email templates and recipients lists are defined here.
Templates need:
'<dict_name>': {
    'subject':Templated email subject string.
    'message':Templated email body string. Accepts HTML formatting.
}

For example:
'example_template': {
    'subject': r'${LINEUP} is updating to version ${VERSION}',
    'message': r'<h2>The ${LINEUP} site will be upated to version ${VERSION}</h2><br>\
                <p>The update will begin in 10 minutes</p><br>\
                <small>This email was auto-generated</small>'
}

Available template items are: ${LINEUP}, ${VERSION}
"""


email_templates = {
    'update_starting': {
        'subject': Template('${LINEUP} update to ${VERSION} will begin in 10 minutes'),
        'message': Template('<h3>The ${LINEUP} site will be updated to ${VERSION}</h3>\
        <p>The update will begin in 10 minutes</p><br>\
        <small>This email is auto-generated</small>')
    },
    'update_complete': {
        'subject': Template('${LINEUP} update to ${VERSION} is complete'),
        'message': Template('<h3>The ${LINEUP} update to ${VERSION} is complete</h3>\
        <p>Post-release testing will begin now</p><br>\
        <small>This email is auto-generated</small>')
    },
    'test_complete': {
        'subject': Template('Post-release testing of ${LINEUP} update to ${VERSION} is complete'),
        'message': Template('<h3>The post-release testing of ${LINEUP} update to ${VERSION} is complete</h3>\
        <p>All tests have passed</p><br>\
        <small>This email is auto-generated</small>')
    }
}


"""
Recipients lists are Python lists of recipient email addresses.
Do not include spaces, and limit each list element to a single email address.
You can include distribution email addresses as well as individual emails.
Each lineup should have it's own <lineup>_recipients list defined.
This lineup name should match the corresponding lineup flag choice defined in send_emails.py.
"""

recipients_dict = {
    'try': ['TryNotify@digitaldefense.com'],
    'fl': ['PatchNotify@digitaldefense.com']
}

# recipients_dict = {
#     'try': ['lee.nix@digitaldefense.com'],
#     'fl': ['lee.nix@digitaldefense.com']
# }


"""
Lineup full name mappings
"""

lineup_dict = {
    'fl': 'Frontline.cloud',
    'try': 'TryFrontline'
}


def craft_email(template_dict, version=None, lineup=None, sender=None, recipients=None, subject=None, message=None):
    """
    Return email object to be sent
    expects sender email, recipients email list,
    subject text
    email body as string
    """

    msg = MIMEMultipart()

    default_email='DDI-TestEng@digitaldefense.com'
    if not version:
        version = '0.0.0.0'
    if not sender:
        sender = default_email
    if not lineup:
        lineup = 'fl'
    if not recipients:
        recipients = ','.join(recipients_dict[lineup])
    if not subject:
        subject = template_dict['subject'].substitute(LINEUP=lineup_dict[lineup], VERSION=version)
    if not message:
        message = template_dict['message'].substitute(LINEUP=lineup_dict[lineup], VERSION=version)

    # setup the parameters of the message
    msg['From'] = sender
    msg['To'] = recipients
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    return sender, recipients, msg.as_string()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Automatically send emails about lineup update status")

    parser.add_argument('version', help='Version being released')
    parser.add_argument('-t', '--template', dest='template', choices=['start', 'done', 'test-complete'], default='start', help='template to use')
    parser.add_argument('-l', '--lineup', dest='lineup', choices=['try', 'fl'], default='fl', help='lineup choice')

    args = parser.parse_args()

    if args.template == 'start':
        template_dict = email_templates['update_starting']
    elif args.template == 'done':
        template_dict = email_templates['update_complete']
    elif args.template == 'test-complete':
        template_dict = email_templates['test_complete']

    server = smtplib.SMTP(host='mail.defense.local')
    sender, recipients, message = craft_email(template_dict,
                                              version=args.version,
                                              lineup=args.lineup)

    server.sendmail(sender, recipients, message)
    server.close()
