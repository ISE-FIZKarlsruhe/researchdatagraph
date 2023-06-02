from pyoxigraph import *
from rich.progress import track
import httpx


def process(hydra_graph):
    members = []
    next = None
    for s, p, o, _ in hydra_graph.quads_for_pattern(
        NamedNode("https://nfdi4culture.de/resource.ttl"), None, None
    ):
        if p == NamedNode("http://www.w3.org/ns/hydra/core#member"):
            members.append(o)
        if p == NamedNode("http://www.w3.org/ns/hydra/core#view"):
            view = o
    for s, p, o, _ in hydra_graph.quads_for_pattern(view, None, None):
        if p == NamedNode("http://www.w3.org/ns/hydra/core#last"):
            if o == view:
                return None, members
        if p == NamedNode("http://www.w3.org/ns/hydra/core#next"):
            next = str(o).strip("<>")
    return next, members


r = httpx.get("https://nfdi4culture.de/resource.ttl?tx_lod_api[limit]=500")
if r.status_code == 200:
    hydra_graph = Store()
    hydra_graph.load(r.content, "text/turtle")

next_view = True
members = []
while next_view:
    next_view, new_members = process(hydra_graph)
    members.extend(new_members)
    print(next_view)
    if next_view:
        r = httpx.get(next_view)
        if r.status_code == 200:
            hydra_graph = Store()
            hydra_graph.load(r.content, "text/turtle")
        else:
            next_view = None

resource_graph = Store()
for resource in track(members):
    r = httpx.get(str(resource).strip("<>"), follow_redirects=True)
    if r.status_code == 200:
        resource_graph.load(r.content, "text/turtle")

print("Serializing", len(resource_graph))
resource_graph.dump("nfdico.nt", "application/n-triples")
