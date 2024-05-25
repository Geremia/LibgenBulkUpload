#!/usr/bin/python3 -u

import csv
import os
import pathlib as pl
import re
import subprocess as sp
import sys
import urllib.parse as up

if len(sys.argv) != 5:
    print("""4 args required:
    relative path of directory of
            (1) files to upload
            (2) uploaded files
            (3) rejected files
    plus: (4) Calibre catalog csv file""")
    exit(1)

upload_dir = './'+sys.argv[1]+'/'
uploaded_dir = './'+sys.argv[2]+'/'
rejects_dir = './'+sys.argv[3]+'/'

print("Specified directories:")
for i in [upload_dir, uploaded_dir, rejects_dir]:
    print(i)
    if not os.path.isdir(i):
        os.mkdir(i)
print()

def sortKey(filename):
    return os.path.getsize(upload_dir+filename)

files = os.listdir(upload_dir)
files = sorted(files, key=sortKey)
if len(files) == 0:
    print("No books to upload.")
    sys.exit(1)

# Process Calibre catalog CSV
nested_list = []
catalog = sys.argv[4]
with open(catalog, mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        nested_list.append(row)

book_catalog = []
with open('Formats.csv', mode='r', newline='', encoding='utf-8-sig') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        book_catalog.append(row)
header = book_catalog[0]

# in Calibre catalog export 
calibre_metadata = [
        '#amazon',
        '#doi',
        '#google',
        '#issn',
        '#lcn',
        '#pubyear',
        'authors',
        'comments',
        'isbn',
        'languages',
        'publisher',
        'series',
        'series_index',
        'tags',
        'title'
        ]

# check that at least 'id' header exists
if 'id' not in header:
    print("Calibre catalog CSV file must have an 'id' column.")
    sys.exit(1)

# corresponding Libgen metadata
libgen_metadata = [
        'asin',
        'doi',
        'gb_id',
        'issn',
        'lcc',
        'year',
        'authors',
        'description',
        'isbn',
        'language',
        'publisher',
        'series',
        'volume',
        'tags',
        'title'
        ]

# Upload books
for f in files:
    upload_dir_f = upload_dir + f
    pat = pl.Path(upload_dir_f).absolute()
    if pat.is_symlink():
        pat = pat.resolve()
    parent = pat.parent.parts[-1]

    try:
        id = re.findall('[0-9]+', parent)[-1]
    except:
        print("No valid Calibre id found for '" + f
              + "' Be sure your uploads directory contains only symlinks to the files in your Calibre library.")
        sys.exit(1)

    try:
        book_entry = [item for item in book_catalog if item[header.index('id')] == str(id)][0]
    except:
        print(id, "wasn't found in Calibre catalog CSV file '" + catalog + "'. Skipping.")
        continue

    env = {}
    for i in range(len(calibre_metadata)):
        try:
            idx = header.index(calibre_metadata[i])
        except:
            continue
        val = up.quote(book_entry[idx])
        if val:
            env[libgen_metadata[i]] = val

    title = up.quote(book_entry[header.index('title')])
    lang = up.quote(book_entry[header.index('languages')])
    process = sp.Popen(['./upload.bash', upload_dir_f, title, lang, 'main'], env=env)
    process.communicate()
    rc = process.returncode
    if rc == 0:  # success
        print("Moving '" + f + "' to '" + uploaded_dir + "'.")
        os.rename(upload_dir_f, uploaded_dir + f)
    else:  # failure
        print("Moving '" + f + "' to '" + rejects_dir + "'.")
        os.rename(upload_dir_f, rejects_dir + f)

