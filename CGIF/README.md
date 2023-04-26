# Culture Graph Interchange Format

https://docs.nfdi4culture.de/ta5-cgif-specification

For the federated acquisition of data for the Culture Knowledge Graph we propose an easy to use, lightweight interchange format based on schema.org for the harvesting of resources from data collections with key attributes (IRIs, names, dates and terms from controlled vocabularies). The Culture Graph Interchange Format (CGIF) has the added benefit of automatically making the data eligible for Google Dataset Search and to significantly improve the findability of websites and datasets through search engine optimization.

## Testing the first version

This section contains some testing of the initial harvested datasets, and mappings to a proposed storage in the Research Data Graph. The first dataset to become available is the [CVMA](https://corpusvitrearum.de/)

Here is [a notebook exploring some of the CVMA data](cvma.ipynb)

## Summary of suggestions

- Make inDefinedTermSet property in the LDJSON an IRI, eg. "schema:inDefinedTermSet": {"@id": "https://iconclass.org/"}

- Add more links to IRIs, not strings. For example also for licenses, and placenames.

- Add links to the "content" metadata, using a property to be decided upon.

## Related Links

https://bioschemas.org/

https://pro.europeana.eu/page/edm-documentation
