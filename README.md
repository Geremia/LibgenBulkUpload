# LibgenBulkUpload
bulk upload files to [http://libgen.la/librarian.php](http://libgen.la/librarian.php) ([Selenium](https://isidore.co/calibre/#panel=book_details&book_id=8602) script)

## Usage
Example:
```bash
./upload.py to_upload uploaded la
```
where `la` is the LibGen top-level domain (TLD). See [below](#libgen-tlds) for the list of supported TLDs.

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

### Libgen TLDs

See [Open SLUM](https://open-slum.pages.dev/) for currently working TLDs.

| Libgen TLD                                    | Country (GeoIP of IPv4 address) |
|-----------------------------------------------|---------------------------------|
| <a href="https://libgen.bz/">bz</a>           | Switzerland 🇨🇭 (Zurich) 
| <a href="https://libgen.gl/">gl</a>           | U.S. 🇺🇸
| <a href="https://libgen.la/">la</a>           | U.S. 🇺🇸
| <a href="https://libgen.li/">li</a>           | Switzerland 🇨🇭 (Zurich)
| <a href="https://libgen.vg/">vg</a>           | Malaysia 🇲🇾

### Populate `upload` folder

The `populate_upload.bash` script will populate the `upload` folder with symlinks to new files in your `~/CalibreLibrary` that you want to upload. It determines the latest upload file based on the newest file in `uploaded`. It uses the formats specified in the (one per line) `formats.txt` file.

The format of the symlinks is:

    TITLE - AUTHOR-randsf.suffix

where "randsf" is a randoom 6 character string; this is to avoid collisions with other files in the `upload` folder. (If you don't want that suffix a part of the AUTHOR name when uploading with `upload.py`, change `upload.py`'s line "`author = re.sub(r'_$', '.', author)`" to "`author = re.sub(r'_$', '.', author)[:-7]`".)

## References

 - [Calibre](https://calibre-ebook.com/)
 - Bodó, Balázs. “[The Genesis of Library Genesis: The Birth of a Global Scholarly Shadow Library](https://www.crimrxiv.com/pub/9tgl8fnu/release/1).” In _CrimRxiv_. Preprint, September 26, 2024.
