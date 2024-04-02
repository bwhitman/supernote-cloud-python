# supernote-cloud-python

python wrapper for unofficial supernote cloud api

tested on "Nomad" (A6X2), works as of april 2024

borrowed from

 * https://github.com/adrianba/supernote-cloud-api/
 * https://github.com/colingourlay/supernote-cloud-api/

combined APIs and turned into Python 

use like

```python
# python
>>> import sync
>>> token = sync.login("email", "password")
>>> sync.file_list(token)

[{'id': 'xxx',
  'directoryId': 'yyy',
  'fileName': 'Note',
  'size': 0,
...
}]

>>> contents = sync.download_file(token, 'zzz') # use id of file from file_list
>>> sync.download_file(token, 'zzz', "filename.note") # saves directly to filename
>>> sync.upload_file(token, "test.pdf", directory="123") # use directory id (not directoryId) from file_list 
```
