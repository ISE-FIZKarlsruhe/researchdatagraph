# NFDI4Culture Research Data Graph

Scripts and notebooks, building the [knowledge graph](https://docs.nfdi4culture.de/ta7-report-2022/services-and-resources/knowledge-graph). For background information, see: [Knowledge Graph-basierte Forschungsdatenintegration in NFDI4Culture](https://zenodo.org/record/7748740)

[Google Doc with discussion on the RDIG](https://docs.google.com/document/d/1YhT8DZqs4boTLPHFuQL4WXLe7M47f6m61ci0CclCafo/edit)

[Miro Board with analysis of metadata](https://miro.com/app/board/uXjVMToHGSI=/)

## Potential Seed Datasources

| Project Name                 | Type        |
| ---------------------------- | ----------- |
| Political Flyers             | RDF/SPARQL  |
| [Linked Stage Graph](/slod/) | RDF/SPARQL  |
| [CVMA](/CGIF/)               | CGIF        |
| Badisch Landesmuseum         | RDF/SPARQL  |
| WissKI                       |             |
| DDB EDM                      | EDM         |
| [Marburg](/marburg/)         | LIDO/CGIF ? |
| [Wikibase](/wikibase/)       | Wikibase    |
| [RADAR](/RADAR/) Repository  | OAI-PMH     |

# Ingest and ETL pipeline

There is currently no procedure in place for how to harvest and ingest data from the different datasets.
In this section we need to add some scripts and solidify the current informal discussions around this topic.

Open topics to seed the discussion:

- pull vs push models.

- update frequencies

- portal-steered data discovery (via ISIL codes?)

- example scripts for ingest/transformation

## Related Links 

[WikiProject NFDI](https://www.wikidata.org/wiki/Wikidata:WikiProject_NFDI)
