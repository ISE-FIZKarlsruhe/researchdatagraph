# Wikibase

There are several projects that use Wikibase as a Research Data Management system. Notably the partner project in TA5 is [Semantic annotation for 3D cultural artefacts](https://wikibase.semantic-kompakkt.de/wiki/Main_Page).
How can we make a semi-standadized interface between the NFDI4Culture Data Graph and such Wikibase systems? Here are some sample queries exploring the data in the above project, to get a feel for what the data looks like, and how we can make a translation step.

The endpoint is: https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql

The query service is: https://query.semantic-kompakkt.de/

[Example Castles](https://tinyurl.com/2hgx7sff)

[Human](https://wikibase.semantic-kompakkt.de/wiki/Item:Q2)

[People](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&o=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q2%3E)

[Person](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&s=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q83%3E)

But then, when I check to see if any of the people are being used as predicates, [zero hits](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&o=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q103%3E)?
So I must be querying it wrong?

Let's start with a [place](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&p=%3Fp&s=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q326%3E)
and [how it is used](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&o=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q326%3E),
and by following all the object links, we eventually get to somehing like:
Painting part in [Mammals - A2 Löwenjagd](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&s=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q124%3E)
But where is that, used? [Using it as an object gives zero hits](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&o=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q124%3E)?

OK, let's use the example query, ["Items that share an Iconclass label"](https://query.semantic-kompakkt.de/embed.html#%23defaultView%3AGraph%0A%0ASELECT%20%3Fitem1%20%3Fitem1Label%20%20%3FiconclassLabel%20%3Ficonclass%20%3Frgb%20%3Frgb2%0AWHERE%0A%7B%0A%20%20%3Fitem1%20tibt%3AP4%20%3Ficonclass.%0A%20%20%3Fitem2%20tibt%3AP4%20%3Ficonclass.%0A%20%20BIND%28%27D88888%27%20as%20%3Frgb%29%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20FILTER%28%3Fitem1%20%21%3D%20%3Fitem2%29%20.%0A%7D%0A)
A [concept "seige"](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&s=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q217%3E&o=%3Fo) which has the Iconclass code 45K21 linked.
What are the [iconographic concepts](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&p=%3Fp&o=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q29%3E) in there?
What are the [Iconclass codes](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&p=%3Chttps%3A//wikibase.semantic-kompakkt.de/prop/direct/P98%3E&o=%3Fo) used?
Which leads us to, [a painting](https://epoz.org/shmarql?e=https://query.semantic-kompakkt.de/proxy/wdqs/bigdata/namespace/wdq/sparql&s=%3Chttps%3A//wikibase.semantic-kompakkt.de/entity/Q343%3E):
