#!/usr/bin/bash

file=${1:?File to upload. Allowed formats: PDF, DJVU, EPUB, MOBI, AZW, AZW3, AZW4, FB2, CHM, RTF, DOC, DOCX, ZIP, RAR, 7Z, CBZ, CBR, CB7.}
title=${2:?Title}
language=${3:?Language}
mainOrFiction=${4:?Upload to \'main\' or \'fiction\'?}
md5sum=`md5sum -z "$file" | sed 's/ .*//'`
upload_url="https://library.bz/$mainOrFiction/upload/"
data_entry_url="https://library.bz/$mainOrFiction/uploads/new/$md5sum"
edit_done_url="https://library.bz/$mainOrFiction/uploads/edit/$md5sum/done"

# All optional and required variables
vars=( "metadata_source" "metadata_query" "title" "volume" "authors" "language" "language_options" "edition" "series" "pages" "year" "publisher" "city" "periodical" "isbn" "issn" "doi" "gb_id" "asin" "ol_id" "ddc" "lcc" "udc" "lbc" "topic" "tags" "cover" "description" "toc" "scan" "dpi" "dpi_select" "sfearchable" "paginated" "page_orientation" "colored" "cleaned" "bookmarks" "file_source" "file_source_issue" "file_commentary" )

# Initialize default values
metadata_source=${metadata_source:-local}
cover=${cover:-$md5sum-g.jpg}
sfearchable=${sfearchable:-1}

# POST only non-null values
data_raw=''
pretty_data_str=''
for var_name in "${vars[@]}"; do
    value="${!var_name}"
    if [ -n "$value" ]; then
        data_raw+="$var_name=$value&"
        pretty_data_str+="\t$var_name: $value\n"
    fi
done
data_raw="${data_raw%'&'}"
pretty_data_str="${pretty_data_str%'\n'}"

echo -e "Uploading '$file' to $upload_url…"
curl "$upload_url" -X POST  \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'  \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'  \
    -H 'Accept-Language: en-US,en;q=0.5'  \
    -H 'Accept-Encoding: gzip, deflate, br, zstd'  \
    -H 'Content-Type: multipart/form-data'  \
    -H 'Origin: https://library.bz'  \
    -H 'Authorization: Basic Z2VuZXNpczp1cGxvYWQ='  \
    -H 'Connection: keep-alive'  \
    -H 'Referer: https://library.bz/main/upload/'  \
    -H 'Upgrade-Insecure-Requests: 1'  \
    -H 'Sec-Fetch-Dest: document'  \
    -H 'Sec-Fetch-Mode: navigate'  \
    -H 'Sec-Fetch-Site: same-origin'  \
    -H 'Sec-Fetch-User: ?1'  \
    -H 'Priority: u=1'  \
    -F "file=@\"$file\"" &> /dev/null

echo -e "Entering data\n$pretty_data_str\nat $data_entry_url…"
curl -L "$data_entry_url" --compressed -X POST  \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0'  \
    -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'  \
    -H 'Accept-Language: en-US,en;q=0.5'  \
    -H 'Accept-Encoding: gzip, deflate, br, zstd'  \
    -H 'Content-Type: application/x-www-form-urlencoded'  \
    -H 'Origin: https://library.bz'  \
    -H 'Authorization: Basic Z2VuZXNpczp1cGxvYWQ='  \
    -H 'Connection: keep-alive'  \
    -H "Referer: $data_entry_url"  \
    -H 'Upgrade-Insecure-Requests: 1'  \
    -H 'Sec-Fetch-Dest: document'  \
    -H 'Sec-Fetch-Mode: navigate'  \
    -H 'Sec-Fetch-Site: same-origin'  \
    -H 'Sec-Fetch-User: ?1'  \
    -H 'Priority: u=1' --data-raw "$data_raw" 2>&1 \
    | grep -zo "The record has been successfully saved." && echo " $edit_done_url" && exit 0

echo -e "Problem with upload (or already uploaded)." && exit 1

