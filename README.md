# LibgenBulkUpload
bulk upload files to [https://library.bz/main/upload/](https://library.bz/main/upload/) (`bash` script)

## Usage
```bash
./upload.bash file_to_upload title two_char_language_code main_or_fiction
```
## Specifying additional metadata

Example
```bash
isbn=9783868386066 authors='Feser, Edward' ./upload.bash Immortal_Souls.pdf 'Immortal Souls: A Treatise on Human Nature' en
```

## Batch with GNU `parallel`

This [GNU `parallel`](https://www.gnu.org/software/parallel/) command uploads (one-at-a-time) all the PDFs in the current directory, assigns their Libgen metadata author to the PDF filename (sans suffix), and sets the language to English:
```bash
parallel -j1 ./upload.bash {} {.} en ::: *.pdf
```

### Metadata

The following metadata can be optionally passed as an environment variable to the script:

 - asin
 - authors
 - bookmarks
 - city
 - cleaned
 - colored
 - cover
 - ddc
 - description
 - doi
 - dpi
 - dpi_select
 - edition
 - file_commentary
 - file_source
 - file_source_issue
 - gb_id
 - isbn
 - issn
 - language
 - language_options
 - lbc
 - lcc
 - metadata_query
 - metadata_source
 - ol_id
 - page_orientation
 - pages
 - paginated
 - periodical
 - publisher
 - scan
 - series
 - sfearchable
 - tags
 - title
 - toc
 - topic
 - udc
 - volume
 - year
