# Persistent Identifiers

When creating LOD resources, we want to use persistent identifiers to ensure a sustainable and FAIR future.
The problem is, which ones? Do we use Handles, DOIS, URNs, Purls, ARKS or plain old vanilla URIs?

One of the options we are investigating for NFDI4Culture, is using [ARK Identifiers](https://arks.org/)

We have a NAAN registred for NFDI4Culture: **ark:/60538/** 🥳

The "raw" functionality of ARK identifiers and the n2t.net resolver is only to redirect identifiers to their destinations, and not to persist metadata. This is one of the downsides compared to a system like the DOI infrastructure.
_But_ can we leverage the Research Data Graph to help in this regard? Can we save metadata for minted PIDs in the RDG, and serve them up as (for example) .ttl files when the resolver is queried via content-negotiation? (and with a well-know prefix, to serve it up as some human-readable form)

Some example code to flesh out this idea to follow... 😎

## Misc Links

[Concept for Setting up the Persistent Identifier Services Working Group in the NFDI Section "Common Infrastructures"](https://zenodo.org/record/6507760)

[Workshop on PIDs within NFDI](https://zenodo.org/record/7635905)

[PID Network DE](https://www.pid-network.de/pids/forschungsdaten)

[Forum Data Publication and Availability #5: Persistent Identifiers](https://nfdi4culture.de/events/forum-data-publication-and-availability-5-persistent-identifiers)

[TIB PID Competence Centre](https://projects.tib.eu/pid-service/en/pid-competence-center/projects-and-publications/)

[Persistent Identification of Instruments](https://www.pidinst.org/)

[PID Overview](https://confluence.csiro.au/display/OFW/PID+Systems) (CSIR Australia)

[PID wijzer](https://www.pidwijzer.nl/) (Dutch)

[Long term sustainablitly of ARKs and federation](https://groups.google.com/g/arks-forum/c/Bx3PMJwLQF0)

[Persistent identifiers for heritage objects](https://journal.code4lib.org/articles/14978) Code4lib Journal Article
