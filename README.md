# LibgenBulkUpload
bulk upload files to [http://libgen.lc/librarian.php](http://libgen.lc/librarian.php) ([Selenium](https://isidore.co/calibre/#panel=book_details&book_id=8602) script)

## Usage
```./upload.py to_upload uploaded rejects```

So title and author metadata is set on LibGen, uploaded files should be in the [Calibre](https://calibre-ebook.com/) format, e.g.:

    TITLE - AUTHOR.suffix

where suffix is one of the LibGen supported formats

 - cbr
 - cbz
 - chm
 - djvu
 - doc
 - docx
 - epub
 - fb2
 - mobi
 - pdf
 - rar
 - rtf
 - zip

e.g.:

    The Nature of Thermodynamics - Bridgman, Percy Williams.djvu
