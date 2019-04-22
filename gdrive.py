from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class GDrive():
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def get_file_list(self):
        filelist = []
        page_token = None

        while True:
            response = self.service.files().list(
                q="trashed = False and 'root' in parents",
                fields='nextPageToken, files(name, id, mimeType)',
                pageToken=page_token).execute()

            filelist = filelist + response.get('files', [])
            page_token = response.get('nextPageToken', None)

            if page_token is None:
                break

        return filelist

    def creat_folder(self):
        file_metadata = {
            'name': 'edenbridge',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['root']
        }
        file = self.service.files().create(
            body=file_metadata, fields='name, id').execute()
        return file

    def upload(self, localfile, mimetype, name, parents='root'):
        file_metadata = {'name': name, 'parents': [parents]}
        media = MediaFileUpload(localfile, mimetype=mimetype)
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='name, id').execute()
        return file

    def download(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))


def main():
    gdrive = GDrive()
    #gdrive.upload('edenbridge.py', 'plain/text', 'edenbridge.py')

    items = gdrive.get_file_list()

    folder = gdrive.creat_folder()
    #
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


if __name__ == '__main__':
    main()