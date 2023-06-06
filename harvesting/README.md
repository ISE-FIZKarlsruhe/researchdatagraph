# Harvesting scripts

This section contains some WIP scripts for harvesting LOD data from the Portal, and initial conversion scripts for harvesting CGIG data.

## Listing datasets to harvest

Can be down by querying the information graph for [a schema:Dataset](https://epoz.org/shmarql?e=https://nfdi4culture.de/sparql&p=%3Chttp%3A//www.w3.org/1999/02/22-rdf-syntax-ns%23type%3E&s=%3Fs&o=%3Chttp%3A//schema.org/Dataset%3E)

## Push vs Pull

One of the ideas mooted at the May 2023 workshop in Mainz was to also allow data providers to upload their data to a Nextcloud folder, in stead of it being harvested. In a sense this still means the data is harvested, but from a WebDAV URL and the NFDI4Culture infra team is suggesting a standardized storage space for participants to use if they do not have their own web space to place data.
