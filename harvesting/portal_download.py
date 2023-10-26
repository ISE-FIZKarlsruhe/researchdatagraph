from pyoxigraph import *
from rich.progress import track
import httpx, time


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
            next = o.value
    return next, members


def main():
    hydra_graph = Store()
    session_graph = Store()
    resource_graph = Store()

    HARVEST_ID = f"harvest_{int(time.time())}"
    H_NODE = NamedNode(f"https://nfdi4culture.de/id/ark:/60538/{HARVEST_ID}")
    session_graph.add(
        Quad(
            H_NODE,
            NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            NamedNode("https://nfdi.fiz-karlsruhe.de/ontology/HarvestSession"),
        )
    )
    session_graph.add(
        Quad(
            H_NODE,
            NamedNode("https://nfdi.fiz-karlsruhe.de/ontology/harvestStartTime"),
            Literal(f"{int(time.time())}"),
        )
    )

    r = httpx.get("https://nfdi4culture.de/resource.ttl?tx_lod_api[limit]=500")
    if r.status_code == 200:
        hydra_graph.load(r.content, "text/turtle")

    next_view = True
    members = []
    while next_view:
        next_view, new_members = process(hydra_graph)
        members.extend(new_members)
        if next_view:
            r = httpx.get(next_view)
            if r.status_code == 200:
                hydra_graph = Store()
                hydra_graph.load(r.content, "text/turtle")
            else:
                next_view = None

    failed_resources = []
    for resource in track(members):
        try:
            r = httpx.get(resource.value, follow_redirects=True)
            if r.status_code == 200:
                resource_graph.load(r.content, "text/turtle")
        except:
            failed_resources.append(resource)
    session_graph.add(
        Quad(
            H_NODE,
            NamedNode("https://nfdi.fiz-karlsruhe.de/ontology/harvestStopTime"),
            Literal(f"{int(time.time())}"),
        )
    )

    for failed_resource in failed_resources:
        session_graph.add(
            Quad(
                H_NODE,
                NamedNode(
                    "https://nfdi.fiz-karlsruhe.de/ontology/resourceRetrievalFailure"
                ),
                failed_resource,
            )
        )

    print("Failed", len(failed_resources))
    print("Serializing", len(resource_graph))
    resource_graph.dump("nfdico.nt", "application/n-triples")
    session_graph.dump(f"{HARVEST_ID}.nt", "application/n-triples")


if __name__ == "__main__":
    main()
