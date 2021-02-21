import dropbox
import os, re
from collections import defaultdict
class DropBox():   

    def __init__(self, conf):
        self.DROPBOX_TOKEN = conf.DROPBOX_TOKEN
    
        self.client = self.auth()

        # self.get_refresh_token()


    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        self.client.close() 


   
    
    def auth(self):
        return dropbox.Dropbox(self.DROPBOX_TOKEN)


    def get_refresh_token(self):
        
       
        old_token = self.client._oauth2_access_token
        self.client.check_and_refresh_access_token()
        new_token = self.client._oauth2_access_token
        # dbx = dropbox.Dropbox(self.DROPBOX_TOKEN, oauth2_refresh_token=, app_key=conf.APP_KEY, app_secret=conf.APP_SECRET)

        print("OLD",old_token)
        print("nEW",new_token)


    async def account_info(self):
        temp = defaultdict(dict)
        
        result =  self.client.users_get_current_account()

        
        temp["abbreviated_name"] = result.name.abbreviated_name
        temp["display_name"] = result.name.display_name
        temp["familiar_name"] = result.name.familiar_name
        temp["given_name"] = result.name.given_name
        temp["surname"] = result.name.surname

        temp['account_id']  = result.account_id
        temp['country'] = result.country
        temp['disabled'] = result.disabled
        temp['email'] = result.email
        temp['email_verified'] = result.email_verified
        temp['is_paired'] = result.is_paired
        temp['locale'] = result.locale
      
        temp['profile_photo_url']  = result.profile_photo_url
        temp['referral_link'] = result.referral_link
        temp['team']  = result.team
        temp['team_member_id'] = result.team_member_id
        return temp
       

    async def list_files(self,
        path,
        recursive=False,
        include_media_info= False,
        include_deleted= False,
        include_has_explicit_shared_members = False,
        include_mounted_folders = True,
        limit=None,
        shared_link=None,
        include_property_groups=None,
        include_non_downloadable_files=True
        ):
        
        response = self.client.files_list_folder(
                    path=path,
                    recursive=recursive,
                    include_media_info=include_media_info,
                    include_deleted=include_deleted,
                    include_has_explicit_shared_members=include_has_explicit_shared_members,
                    include_mounted_folders=include_mounted_folders,
                    limit=limit,
                    shared_link= shared_link,
                    include_property_groups=include_property_groups,
                    include_non_downloadable_files=include_non_downloadable_files)
        temp ={}
        

        for file in response.entries:

            link = self.client.sharing_create_shared_link(file.path_display)
     
            path = link.url.replace("0", "1")
            temp[file.path_display] = path
         
        return temp

    async def upload_file(self, file_from, file_to):
        
        with  open(file_from, 'rb') as f:

            self.client.files_upload(f.read(), file_to)
            
       

    
    async def save_file_localy(self, file_path,filename):

        metadata, res = self.client.files_download(file_path+filename)

        with open(metadata.name, "wb") as f:
            f.write(res.content)


    async def get_link_of_file(self, file_path, filename, dowload=False):
        
        path = self.client.sharing_create_shared_link(file_path+filename)
        if dowload:
            path = path.url.replace("0", "1")

        return {"file":path.url}




