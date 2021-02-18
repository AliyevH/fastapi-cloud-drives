from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http, io
from googleapiclient.discovery import build
from oauth2client import file, client, tools

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class GoogleDrive:   
    def __init__(self, conf):
        self.STORAGE_JSON = "storage.json"
        self.CLIENT_ID_JSON = conf.CLIENT_ID_JSON
        self.SCOPES = conf.SCOPES
        self.creds = None

        self.auth()
        

    def auth(self):
        """[Google Drive API Authentication]
        """
        self.store = file.Storage(self.STORAGE_JSON)
        self.creds = self.store.get()

        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(self.CLIENT_ID_JSON, self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)

        self.build_service()


    def build_service(self):
        """[Building drive v3]
        """
        self.drive_service = build('drive', 'v3', credentials=self.creds)


    async def list_files(self,
        q: str = "",
        corpora: str = "",
        includeItemsFromAllDrives: bool = False,
        supportsAllDrives: bool = False,
        pageSize: int = 100,
        spaces: str = "drive",
        fields: str = None
    ):
        """[Get files from Google Drive]
    
        Returns:
            [list of dictionary]: [{}, {}] or str(err)
        
        Args:
            q (str): [
                "mimeType='image/jpeg'"
                "name contains 'Resume'"
                Default= ""
                ]

        corpora (str):  [user, drive, allDrives]

        includeItemsFromAllDrives (bool):

        supportsAllDrives (bool): [Default is False]

        pageSize (int): [1-1000, Default 100]

        spaces (str): [drive, appDataFolder, photos]

        fields (str):        

        orderBy (str): [
            createdTime, folder, modifiedByMeTime,modifiedTime, 
            name, name_natural, quotaBytesUsed, recency, sharedWithMeTime,
            starred, viewedByMeTime, desc
            ]

        Returns:
            [List of files metadata]: [All files metadata is dictionary]
        """
        try:
            __file = self.drive_service.files().list(
                q=q, 
                corpora=corpora,
                includeItemsFromAllDrives=includeItemsFromAllDrives,
                supportsAllDrives=supportsAllDrives,
                pageSize=pageSize,
                spaces=spaces,
                fields=fields,
                ).execute().get('files', [])
            return __file
        except Exception as err:
            return str(err)


    async def upload_file(self, filename: str, filepath: str, mimetype=None):
        """[Upload file to google drive]

        Args:
            filename (str): [fielname is used to create file in google drive]
            filepath (str): [filepath to file which to upload]
            mimetype ([type], optional): [Google detects it automatically]. Defaults to None.

        Returns:
            [str]: [ID of file created in Google Drive]
        """
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
        """[Create folder in Google Drive]

        Args:
            folder_name (str): [Name of folder to create]

        Returns:
            [str]: [ID of created folder]
        """
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


    async def download_file(self, file_id: str = None, file_name: str = None):
        """[Download File]

        Args:
            file_id (str, optional): [Download by file ID]. Defaults to None.
            file_name (str, optional): [Download by file name]. Defaults to None.

        Returns:
            [func]: [Returns private functions to download file]
        """
        if file_id:
            return await self.__download_file_by_id(file_id=file_id)
        elif file_name:
            return await self.__download_file_by_name(file_name=file_name)


    async def __download_file_by_id(self, file_id):
        """[Download file by id]

        Args:
            file_id ([str]): [ID of file in Google Drive]

        Returns:
            [str]: [Status of file. Example: Downloaded or file not found]
        """
        __file_name = None

        f = await self.list_files()
        for i in f:
            if i.get("id") == file_id:
                __file_name = i.get("name")
                break
            
        if not __file_name:
            return "File not found"
        
        request = self.drive_service.files().get_media(fileId=file_id) 

        fh = io.FileIO(__file_name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        return f"{__file_name} downloaded"


    async def __download_file_by_name(self, file_name):
        """[Download file by name. By default it searches file with exact name. If founds calls private method to download this file by ID]

        Args:
            file_name ([str]): [Name of a file to download]

        Returns:
            [func]: [Returns private function to download file by ID]
            [str]: [File not found]
        """

        f = await self.list_files(
            q=f"name = '{file_name}'"
        )
        
        if f:
            return await self.__download_file_by_id(f[0].get("id"))

        return "File not Found"
        
