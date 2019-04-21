from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload


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
         # Call the Drive v3 API
        filelist = self.service.files().list(q="trashed=False and 'root' in parents", pageSize=10, fields="nextPageToken, files(mimeType, id, name, parents)").execute()
        #return filelist.get('files', [])
        return filelist
        
    def upload(self, localfile, mimetype, name_on_gdrive, parents=None):
        if parents is not None:
            file_metadata = {'name': name_on_gdrive, 'parents': [parents]}
        else:
            file_metadata = {'name': name_on_gdrive}
        media = MediaFileUpload(localfile, mimetype=mimetype)
        file = self.service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields='id').execute()
        return file.get('id')

def main():
    gdrive = GDrive()   
    #gdrive.upload('edenbridge.py', 'plain/text', 'edenbridge.py')
    
    items = gdrive.get_file_list()
#
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    

if __name__ == '__main__':
    main()