# University Library Heidelberg

UniBib Heidelberg offers the following OAI-PMH interfaces: https://www.ub.uni-heidelberg.de/helios/kataloge/datenschnittstellen.html (Section OAI-PMH)

There is a mapping to a standard vocabulary - GND subjects, as e.g., here in this example: https://books.ub.uni-heidelberg.de/index.php/index/oai?verb=ListRecords&metadataPrefix=oai_dc&set=arthistoricum:caa

Also, RDF (including persistent URIs), as e.g. here: https://katalog.ub.uni-heidelberg.de/cgi-bin/titel.cgi?katkey=67075690&format=xml&format2=rdf or MODS (including more metadata) https://katalog.ub.uni-heidelberg.de/cgi-bin/titel.cgi?katkey=67075690&format=xml&format2=mods

Looks like the MODS has the most useful metadata, the RDF output is very sparse.
Probably feasible to use the [BEACON interface](https://katalog.ub.uni-heidelberg.de/beacon.txt) combined with MODS to make a useful extract.
