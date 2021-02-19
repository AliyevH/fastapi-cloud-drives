from abc import ABC, abstractmethod
 
class CloudStorageAbstractClass(ABC):
 
    # def __init__(self):
    #     super().__init__()
    
    @abstractmethod
    def auth(self):
        pass

    @abstractmethod
    def build_service(self):
        pass

    @abstractmethod
    def list_files(self):
        pass

    @abstractmethod
    def upload_file(self):
        pass

    @abstractmethod
    def create_folder(self):
        pass

    @abstractmethod
    def download_file(self):
        pass
