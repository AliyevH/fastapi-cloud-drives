from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class GoogleDrive:   
    def __init__(self, conf):
        self.STORAGE_JSON = conf.STORAGE_JSON
        self.CLIENT_ID_JSON = conf.CLIENT_ID_JSON
        self.SCOPES = conf.SCOPES
        self.creds = None
        self.auth()
        

    def auth(self):
        self.store = file.Storage(self.STORAGE_JSON)
        self.creds = self.store.get()

        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(self.CLIENT_ID_JSON, self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)

        self.build_service()

    # def auth(self):
        
    #     if os.path.exists('token/token.pickle'):
    #         with open('token/token.pickle', 'rb') as token:
    #             self.creds = pickle.load(token)

    #     # If there are no (valid) credentials available, let the user log in.
    #     if not self.creds or not self.creds.valid:
    #         if self.creds and self.creds.expired and self.creds.refresh_token:
    #             self.creds.refresh(Request())
    #         else:
    #             flow = InstalledAppFlow.from_client_secrets_file(
    #                 'token/client_id.json', self.SCOPES)
    #             self.creds = flow.run_local_server(port=0)
    #         # Save the credentials for the next run
    #         with open('token/token.pickle', 'wb') as token:
    #             pickle.dump(self.creds, token)

    #     self.build_service()

    def build_service(self):
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    async def list_files(self,
        q: str = "",
        corpora: str = "",
        includeItemsFromAllDrives: bool = False,
        supportsAllDrives: bool = False,
        pageSize: int = 100,
        spaces: str = "drive"
    ):
        """[Get files from Google Drive]
    
        Returns:
            [list of dictionary]: [{}, {}] or str(err)
        
        Possible options:

        q[str]: "mimeType='image/jpeg'"
                "name contains 'Resume'"
                Default= ""

        corpora[str]:  user, drive, allDrives

        includeItemsFromAllDrives[bool]:

        supportsAllDrives[bool]: Default: False

        pageSize[int]: 1-1000, Default 100

        spaces[str]: drive, appDataFolder, photos

        fields[str]:        

        orderBy[str]: createdTime, folder, modifiedByMeTime,modifiedTime, 
                      name, name_natural, quotaBytesUsed, recency, sharedWithMeTime,
                      starred, viewedByMeTime, desc
        """
        try:
            __file = self.drive_service.files().list(
                q="fullText contains 'docker'", 
                corpora=corpora,
                includeItemsFromAllDrives=includeItemsFromAllDrives,
                supportsAllDrives=supportsAllDrives,
                pageSize=pageSize,
                spaces=spaces
                ).execute().get('files', [])
            return __file
        except Exception as err:
            return str(err)

    async def upload_file(self, filename: str, filepath: str, mimetype=None):
        __file = self.drive_service.files()

        file_metadata = {"name" : filename}

        media = MediaFileUpload(
            filepath,
            mimetype=mimetype,
            )
        try:
            __drive_file = __file.create(
                body=file_metadata,
                media_body=media,
                fields='id'
                ).execute()
            return __drive_file.get("id")
        except Exception as err:
            return str(err)

    async def create_folder(self, folder_name: str):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        try:
            __file = self.drive_service.files().create(
                body=file_metadata,
                fields='id'
                ).execute()
            return __file.get("id")
        except Exception as err:
            return str(err)