# LibgenBulkUpload
bulk upload files to [http://libgen.la/librarian.php](http://libgen.la/librarian.php) ([Selenium](https://isidore.co/calibre/#panel=book_details&book_id=8602) script)

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

### Populate `upload` folder

The `populate_upload.bash` script will populate the `upload` folder with symlinks to new files in your `~/CalibreLibrary` that you want to upload. It determines the latest upload file based on the newest file in `uploaded`. It uses the formats specified in the (one per line) `formats.txt` file.

## References

 - [Calibre](https://calibre-ebook.com/)
 - Bodó, Balázs. “[The Genesis of Library Genesis: The Birth of a Global Scholarly Shadow Library](https://www.crimrxiv.com/pub/9tgl8fnu/release/1).” In _CrimRxiv_. Preprint, September 26, 2024.
