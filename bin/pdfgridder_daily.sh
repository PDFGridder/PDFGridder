#!/bin/sh

pg_dump -U web -Fc pdfgridder > /tmp/pdfgridder_daily.db && s3cmd put --acl-private /tmp/pdfgridder_daily.db s3://pdfgridder.org/pdfgridder_daily.db > /dev/null

find /var/www/pdfgridder/pdfgridder/site_media/media/grids* -mtime +30 -exec rm {} \;
