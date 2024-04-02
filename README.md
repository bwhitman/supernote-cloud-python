# supernote-cloud-python

Python wrapper for unofficial [supernote cloud](https://support.supernote.com/en_US/Tools-Features/supernote-cloud) api

tested on ["Nomad" (A6X2)](https://supernote.com/products/supernote-nomad), works as of april 2024. no guarantees!

Borrowed from

 * https://github.com/adrianba/supernote-cloud-api/
 * https://github.com/colingourlay/supernote-cloud-api/

combined those two APIs and turned into Python so it is easier to use in scripts

use it like

```python
>>> import supernote
>>> token = supernote.login("email", "password")
>>> supernote.file_list(token)

[{'id': 'xxx',
  'directoryId': 'ccc',
  'fileName': 'Note',
  'size': 0,
...
}]

# use id of directory (not directoryId) to see sub directory contents
>>> supernote.file_list(token, 'xxx') 

[{'id': 'bbb',
  'directoryId': 'ccc',
  'fileName': 'design.note',
  'size': 160760,
...
}]

# use id of file from file_list
>>> contents = supernote.download_file(token, 'bbb')

# saves directly to filename
>>> supernote.download_file(token, 'bbb', "filename.note")

# use id of directory (not directoryId) from file_list 
>>> supernote.upload_file(token, "test.pdf", directory="xxx")
```
