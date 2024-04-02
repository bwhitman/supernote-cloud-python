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

## Download NYT crossword puzzle PDF and upload to Supernote cloud

A popular thing to do on Supernotes is play the NYT puzzle with a pen, like the olden days. There's a few scripts that claim to do this but they rely on Dropbox instead of the built in cloud sync, and they all fail these days as NYT has changed how downloading PDFs work on their site. 

If you have a NYT sub, copy your cookies into `auth.txt` in this folder, and then make sure your `Document` folder in Supernote has a `puzzles` folder inside:

```
# your auth.txt file in the current folder should have
# supernote-email,password
# NYT-cookie0 (load the NYT page and copy your cookies)
# NYT-cookie1 ("print" a crossword and copy your cookies from that request)
```

Then just:

```
python supernote.py
```

