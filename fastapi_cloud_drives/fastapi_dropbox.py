import dropbox
from pydantic import BaseModel,  BaseSettings
from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)


dbx = dropbox.Dropbox('sl.ArkQYUcUBxWd7mrPlD6xTn7y1VBPjqv6k6RvmkOY2haUy2SxN24V-OKszd-5_9i5oM1KuVfMD9ijLpStd3cumD05HjZABv6vrhKw9pNJf-9k9qcIoAIPKM2IQb6wdKNq87DrCZI')
print(dbx.users_get_current_account())





a = DropBoxConfig()
print(a)

