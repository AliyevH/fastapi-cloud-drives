from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleDrive:   
    def __init__(self, conf):
        self.STORAGE_JSON = conf.STORAGE_JSON
        self.CLIENT_ID_JSON = conf.CLIENT_ID_JSON
        self.SCOPES = conf.SCOPES
        self.auth()

    def auth(self):
        self.store = file.Storage(self.STORAGE_JSON)
        self.creds = self.store.get()

        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets(self.CLIENT_ID_JSON, self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)

        self.build_drive()

    def build_drive(self):
        self.DRIVE = discovery.build('drive', 'v3', http=self.creds.authorize(Http()))


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
            response = self.DRIVE.files().list(
                q="fullText contains 'docker'", 
                corpora=corpora,
                includeItemsFromAllDrives=includeItemsFromAllDrives,
                supportsAllDrives=supportsAllDrives,
                pageSize=pageSize,
                spaces=spaces
                ).execute().get('files', [])
            return response
        except Exception as err:
            return str(err)