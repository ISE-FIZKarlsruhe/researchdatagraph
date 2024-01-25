# LIDO to RDF conversion

Read in a collection of LIDO XML files stored in a directory, and converts the data to a single RDF in N-triles format ready for ingestion.
Uses the [LIDOlator library](https://github.com/epoz/lidolator) for convenient parsing of the XML data to a Python dict.

Some example invocations:

```
DEBUG=1 OUTPATH=bar INPATH=foo PUBLISHER_IRI=https://nfdi4culture.de/id/E1979/ SOURCE_URI_TEMPLATE='https://heidicon.ub.uni-heidelberg.de/api/v1/plugin/base/oai/oai?verb=GetRecord&metadataPrefix=lido&identifier=__objid__' MAX_COUNT=999  python src/transform/lido/main.py
```

or:

```
DEBUG=1 OUTPATH=bar INPATH=foo PUBLISHER_IRI=https://nfdi4culture.de/id/E2916 SOURCE_URI_TEMPLATE='https://api.deutsche-digitale-bibliothek.de/items/__objid__/source/record' OBJID_PREFIX=https://deutsche-digitale-bibliothek.de/item/ MAX_COUNT=999  python src/transform/lido/main.py
```
