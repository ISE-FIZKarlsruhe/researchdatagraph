# University Library Heidelberg

UniBib Heidelberg offers the following OAI-PMH interfaces: https://www.ub.uni-heidelberg.de/helios/kataloge/datenschnittstellen.html (Section OAI-PMH)

There is a mapping to a standard vocabulary - GND subjects, as e.g., here in this example: https://books.ub.uni-heidelberg.de/index.php/index/oai?verb=ListRecords&metadataPrefix=oai_dc&set=arthistoricum:caa

Also, RDF (including persistent URIs), as e.g. here: https://katalog.ub.uni-heidelberg.de/cgi-bin/titel.cgi?katkey=67075690&format=xml&format2=rdf or MODS (including more metadata) https://katalog.ub.uni-heidelberg.de/cgi-bin/titel.cgi?katkey=67075690&format=xml&format2=mods

Looks like the MODS has the most useful metadata, the RDF output is very sparse.
Probably feasible to use the [BEACON interface](https://katalog.ub.uni-heidelberg.de/beacon.txt) combined with MODS to make a useful extract.

---

## What kind of IDs should we choose to map uniqueness?

Should we use the OAI-PMH ID, some kind of inventory number, or the linked URI?

Consider these two records:

[1832908b-d9a8-4def-a184-d442b56e4087](https://heidicon.ub.uni-heidelberg.de/api/v1/plugin/base/oai/oai?verb=GetRecord&metadataPrefix=lido&identifier=oai:heidicon.ub.uni-heidelberg.de:1832908b-d9a8-4def-a184-d442b56e4087)

and 

[03716d2c-8b8e-4316-a5c7-b35b24ad969e](https://heidicon.ub.uni-heidelberg.de/api/v1/plugin/base/oai/oai?verb=GetRecord&metadataPrefix=lido&identifier=oai:heidicon.ub.uni-heidelberg.de:03716d2c-8b8e-4316-a5c7-b35b24ad969e)

They are different OAI IDs, but [both refer](https://nfdi.fiz-karlsruhe.de/shmarql?e=_local_&p=%3Fp&o=%3Chttps%3A//heidicon.ub.uni-heidelberg.de/detail/741164%3E) to [the same page](https://heidicon.ub.uni-heidelberg.de/detail/741164) - the LIDO files are also almost exactly the same.

