from abc import ABC, abstractclassmethod, abstractmethod
from abc import abstractproperty
 
class CloudStorageAbstractClass(ABC):
    
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

    @abstractclassmethod
    def list_all_buckets(self):
        pass
