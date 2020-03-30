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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Email:
    def __init__(self, config):
        super().__init__()
        self.config = config
        try:
            self.session = smtplib.SMTP_SSL(
                self.config['smtp_add'],
                self.config['smtp_port'])
            self.session.ehlo()
            self.session.login(
                self.config['username'], self.config['password'])
        except Exception as e:
            # Print any error messages to stdout
            print(e)

    def init_mail_body(self, to_add, subject):
        # Prepare Mail Body
        mail_body = MIMEMultipart()
        mail_body['From'] = self.config['from_add']
        mail_body['To'] = to_add
        mail_body['Subject'] = subject
        return mail_body

    # Call this to send plain text emails.
    # plain or html
    def send_email(self, to_add, Subject, txtMessage,
                   msg_type='plain',
                   path=None,
                   file_name=None):
        mail_body = self.init_mail_body(to_add, Subject)
        # Attach Mail Message
        msg = MIMEText(txtMessage, msg_type)
        mail_body.attach(msg)

        if path is not None:
            # open the file to be sent
            attachment = open(path, "rb")

            # instance of MIMEBase
            mime = MIMEBase('application', 'octet-stream')

            # change the payload into encoded form
            mime.set_payload((attachment).read())

            # encode into base64
            encoders.encode_base64(mime)

            mime.add_header('Content-Disposition',
                            "attachment; filename= %s" % file_name)

            # attach mime to mail_body
            mail_body.attach(mime)

        # Send Mail
        self.session.sendmail(
            self.config['from_add'],
            [to_add],
            mail_body.as_string())

    def __del__(self):
        self.session.close()
        del self.session


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
