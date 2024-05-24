# LibgenBulkUpload
bulk upload files to [https://library.bz/main/upload/](https://library.bz/main/upload/)

## Usage
```bash
./upload.bash file_to_upload title language_code main_or_fiction
```
### Specifying additional metadata

Example
```bash
isbn=9783868386066 authors='Feser, Edward' ./upload.bash Immortal_Souls.pdf 'Immortal Souls: A Treatise on Human Nature' eng main
```

### Batch with GNU `parallel`

This [GNU `parallel`](https://www.gnu.org/software/parallel/) command uploads (one-at-a-time) all the PDFs in the current directory, assigns their Libgen metadata author to the PDF filename (sans suffix), and sets the language to English:
```bash
parallel -j1 ./upload.bash {} {.} eng main ::: *.pdf
```

### Metadata

The following metadata can be optionally passed as an environment variable to the script:

 - `asin`, `authors`, `bookmarks`, `city`, `cleaned`, `colored`, `cover`, `ddc`, `description`, `doi`, `dpi`, `dpi_select`, `edition`, `file_commentary`, `file_source`, `file_source_issue`, `gb_id`, `isbn`, `issn`, `language`, `language_options`, `lbc`, `lcc`, `metadata_query`, `metadata_source`, `ol_id`, `page_orientation`, `pages`, `paginated`, `periodical`, `publisher`, `scan`, `series`, `sfearchable`, `tags`, `title`, `toc`, `topic`, `udc`, `volume`, `year`

## Calibre

If you [export a CSV catalog from Calibre](https://manual.calibre-ebook.com/gui.html#catalogs), you can use it with `calibre.py` to feed in the metadata for bulk book uploads, automatically. Be sure the first (left-most) column is the Calibre `id`. The specified "files to upload" directory is expected to contain symlinks to the files in your Calibre library.

To setup the symlinks, execute a command like this in your upload directory:
```bash
for i in `cat ../formats.txt`;
do
    find ~/Calibre\ Library/ -type f -iname "*.$i" -print0 | \
        xargs -0 -I{} sh -c 'filename=`basename "{}"`;
            random_part=$(mktemp -u XXXXXX);
            suffix=".${filename##*.}";
            newname="${filename%.*}-${random_part}${suffix}";
            ln -sv "{}" "$newname";'
done 
```

<sup>`calibre.py` is a similar script to the old `upload.py` Selenium script.</sup>
