# supernote-cloud-python

Python wrapper for unofficial [supernote cloud](https://support.supernote.com/en_US/Tools-Features/supernote-cloud) api

tested on ["Nomad" (A6X2)](https://supernote.com/products/supernote-nomad), works as of april 2024. no guarantees!

Borrowed from

 * https://github.com/adrianba/supernote-cloud-api/
 * https://github.com/colingourlay/supernote-cloud-api/

combined those two APIs and turned into Python so it is easier to use in scripts

use it like

```python
>>> import sync
>>> token = sync.login("email", "password")
>>> sync.file_list(token)

[{'id': 'xxx',
  'directoryId': 'yyy',
  'fileName': 'Note',
  'size': 0,
...
}]

>>> sync.file_list(token, 'aaa') # use id of directory (not directoryId) to see sub directory contents

[{'id': 'bbb',
  'directoryId': 'ccc',
  'fileName': 'design.note',
  'size': 160760,
...
}]

>>> contents = sync.download_file(token, 'bbb') # use id of file from file_list

>>> sync.download_file(token, 'bbb', "filename.note") # saves directly to filename

>>> sync.upload_file(token, "test.pdf", directory="123") # use id of directory (not directoryId) from file_list 
```
