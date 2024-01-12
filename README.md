# NFDI4Culture Research Data Graph

## RDG Barnraising September 2023

See: https://docs.google.com/document/d/1iVftXSV_5lcHP9E5Hl5kxaaXXVjyLdNYVMLr5G1z0xo/edit

---

Scripts and notebooks, building the [knowledge graph](https://docs.nfdi4culture.de/ta7-report-2022/services-and-resources/knowledge-graph). For background information, see: [Knowledge Graph-basierte Forschungsdatenintegration in NFDI4Culture](https://zenodo.org/record/7748740)

[Google Doc with discussion on the RDG](https://docs.google.com/document/d/1YhT8DZqs4boTLPHFuQL4WXLe7M47f6m61ci0CclCafo/edit)

[Miro Board with analysis of metadata](https://miro.com/app/board/uXjVMToHGSI=/)

## Potential Seed Datasources

| Project Name                    | Type        |
| ------------------------------- | ----------- |
| Political Flyers                | RDF/SPARQL  |
| [Linked Stage Graph](/slod/)    | RDF/SPARQL  |
| [CVMA](/CGIF/)                  | CGIF        |
| Badisch Landesmuseum            | RDF/SPARQL  |
| WissKI                          |             |
| [DDB](/DDB/)                    | EDM         |
| [Marburg](/marburg/)            | LIDO/CGIF ? |
| [Wikibase](/wikibase/)          | Wikibase    |
| [RADAR](/RADAR/) Repository     | OAI-PMH     |
| [Univ Heidelberg](/heidelberg/) | OAI-PMH/RDF |
| [RISM](/rism/)                  | RDF/SPARQL  |
| [MiMoText](/mimotext/)          | Wikibase    |

# Ingest and ETL pipeline

There is currently no procedure in place for how to harvest and ingest data from the different datasets.
In this section we need to add some scripts and solidify the current informal discussions around this topic.

Open topics to seed the discussion:

- pull vs push models.

- update frequencies

- portal-steered data discovery (via ISIL codes?)

- example scripts for ingest/transformation

- [Hydra Scraper](https://gitlab.rlp.net/adwmainz/digicademy/cvma/hydra-scraper): generic command-line tool; originally produced to test CVMA data; can compile dumps of CGIF lists (and other Hydra-paginated APIs), produce beacons of all individual resources based on those lists, and compile dumps of those resources; 0.7.1 will be the debugged version

## Related Links

[WikiProject NFDI](https://www.wikidata.org/wiki/Wikidata:WikiProject_NFDI)
