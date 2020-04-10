#!/usr/bin/env python3
"""
    Project Edenbridge
    Copyright (C) 2019 - 2020  Zhengyu Peng

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def init_mail_body(mail_body, attachment=None):
    # Prepare Mail Body
    m_body = MIMEMultipart()
    m_body['From'] = mail_body['from']
    m_body['To'] = mail_body['to']
    m_body['Subject'] = mail_body['subject']

    msg = MIMEText(mail_body['message'], mail_body['type'])
    m_body.attach(msg)

    if attachment is not None:
        data_folder = Path(attachment['path'])
        full_path = data_folder / attachment['file_name']
        # open the file to be sent
        att = open(full_path, "rb")

        # instance of MIMEBase
        mime = MIMEBase('application', 'octet-stream')

        # change the payload into encoded form
        mime.set_payload((att).read())

        # encode into base64
        encoders.encode_base64(mime)

        mime.add_header('Content-Disposition',
                        "attachment; filename= %s" % attachment['file_name'])

        # attach mime to mail_body
        m_body.attach(mime)

    return m_body


def send_email(mail_server, mail_body, attachment=None):
    body = init_mail_body(mail_body, attachment)

    try:
        session = smtplib.SMTP_SSL(
            mail_server['smtp_add'],
            mail_server['smtp_port'])
        session.ehlo()
        session.login(
            mail_server['username'], mail_server['password'])

        # Send Mail
        session.sendmail(
            mail_body['from'],
            [mail_body['to']],
            body.as_string())

        session.quit()

    except Exception as e:
        # Print any error messages to stdout
        print(e)


'''

    `                      `
    -:.                  -#:
    -//:.              -###:
    -////:.          -#####:
    -/:.://:.      -###++##:
    ..   `://:-  -###+. :##:
           `:/+####+.   :##:
    .::::::::/+###.     :##:
    .////-----+##:    `:###:
     `-//:.   :##:  `:###/.
       `-//:. :##:`:###/.
         `-//:+######/.
           `-/+####/.
             `+##+.
              :##:
              :##:
              :##:
              :##:
              :##:
               .+:

'''
