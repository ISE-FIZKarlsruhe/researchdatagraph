import multiprocessing, sqlite3, time, gzip, rdflib, sys, os, traceback
import xxhash
from xml.etree import ElementTree as ET
from rich import print
import pyoxigraph as px
from urllib.parse import quote

PREFIXES = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "ore": "http://www.openarchives.org/ore/terms/",
    "edm": "http://www.europeana.eu/schemas/edm/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "cidoc": "http://www.cidoc-crm.org/rdfs/cidoc_crm_v5.0.2_english_label.rdfs#",
    "ddbedm": "http://www.deutsche-digitale-bibliothek.de/edm/",
    "ddbitem": "http://www.deutsche-digitale-bibliothek.de/item/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
}


OUTPUT_DIR = sys.argv[2]


def filepath_from(objid):
    objid = str(objid)
    level1 = os.path.join(OUTPUT_DIR, objid[:2])
    level2 = os.path.join(OUTPUT_DIR, objid[:2], objid[:5])
    for x in (level1, level2):
        if not os.path.exists(x):
            try:
                os.mkdir(x)
            except:
                ...
    return os.path.join(level2, objid)


def NN(val):
    try:
        return px.NamedNode(val)
    except:
        return px.Literal(val)


def lido_to_rdf(objid, xml):
    t = []
    ta = t.append

    ns1 = "{http://www.lido-schema.org}"
    doc = ET.fromstring(xml)

    subj = f"https://deutsche-digitale-bibliothek.de/item/{objid}"
    ta(
        (
            px.NamedNode("http://schema.org/publisher"),
            px.NamedNode("https://nfdi4culture.de/id/E2916"),
        )
    )

    for recordInfoLink in doc.findall(
        f".//{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordInfoSet/{ns1}recordInfoLink"
    ):
        subj = recordInfoLink.text
        ta((px.NamedNode("http://schema.org/url"), NN(recordInfoLink.text)))

    for image in doc.findall(
        f".//{ns1}administrativeMetadata/{ns1}resourceWrap/{ns1}resourceSet/{ns1}resourceRepresentation/{ns1}linkResource"
    ):
        ta((px.NamedNode("http://schema.org/image"), NN(image.text)))

    category = doc.find(f".//{ns1}category/{ns1}conceptID")
    objectWorkType = doc.find(
        f".//{ns1}descriptiveMetadata/{ns1}objectClassificationWrap/{ns1}objectWorkTypeWrap/{ns1}objectWorkType/{ns1}conceptID"
    )
    title = doc.find(
        f".//{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}titleWrap/{ns1}titleSet/{ns1}appellationValue"
    )
    legalBody = doc.findall(
        f".//{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}repositoryWrap/{ns1}repositorySet/{ns1}repositoryName/{ns1}legalBodyID"
    )
    subjects = doc.findall(
        f".//{ns1}descriptiveMetadata/{ns1}objectRelationWrap/{ns1}subjectWrap/{ns1}subjectSet/{ns1}subject/{ns1}subjectConcept/{ns1}conceptID"
    )
    materials = doc.findall(
        f"{ns1}descriptiveMetadata/{ns1}eventWrap/{ns1}eventSet/{ns1}event/{ns1}eventMaterialsTech/{ns1}materialsTech/{ns1}termMaterialsTech/{ns1}conceptID"
    )
    # we are combining them all into the schema:keywords...
    subjects.extend(materials)

    mdate = doc.find(
        f"{ns1}descriptiveMetadata/{ns1}eventWrap/{ns1}eventSet/{ns1}event/{ns1}eventDate/{ns1}displayDate"
    )

    description = doc.find(
        f".//{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}objectDescriptionWrap/{ns1}objectDescriptionSet/{ns1}descriptiveNoteValue"
    )
    rid = doc.find(f".//{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordID")
    if objectWorkType is not None and objectWorkType.text:
        ta(
            (
                px.NamedNode("https://nfdi4culture.de/ontology#objectWorkType"),
                NN(objectWorkType.text),
            )
        )
    if title is not None and title.text:
        # Get the language from the xml:lang="de"
        language = title.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
        if language:
            title_literal = px.Literal(title.text, language=language)
        else:
            title_literal = px.Literal(title.text)

        ta(
            (
                px.NamedNode("http://schema.org/name"),
                title_literal,
            )
        )
    if description is not None and description.text:
        ta(
            (
                px.NamedNode("http://purl.org/dc/terms/description"),
                px.Literal(description.text),
            )
        )
    for lb in legalBody:
        if lb.text:
            ta(
                (
                    px.NamedNode("http://schema.org/publisher"),
                    NN(lb.text),
                )
            )
    for subject in subjects:
        if subject.text:
            st = subject.text
            if subject.text.startswith("http://iconclass.org/"):
                st = "http://iconclass.org/" + quote(subject.text[21:])
            try:
                ta(
                    (
                        px.NamedNode("http://schema.org/keywords"),
                        NN(st),
                    )
                )
            except:
                traceback.print_exc()
                print("IRI Encoding problem" + repr(subject.text))

    if mdate is not None and mdate.text:
        ta(
            (
                px.NamedNode("http://purl.org/dc/elements/1.1/date"),
                px.Literal(mdate.text),
            )
        )

    # As the first version of proving the PID theory, use xxhash of the URI here!
    subj_hash = xxhash.xxh64(f"<{subj}>").intdigest()

    return (
        px.NamedNode(f"https://nfdi4culture.de/id/ark:/60538/{subj_hash}"),
        t,
    )


def process(objid, xml):
    xml = gzip.decompress(xml)
    g = rdflib.Graph()
    for k, v in PREFIXES.items():
        g.namespace_manager.bind(k, rdflib.URIRef(v))

    doc = ET.fromstring(xml)
    # edm = doc.find(".//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")
    # g.parse(data=ET.tostring(edm), format="application/rdf+xml")
    # edm = g.serialize(format="turtle")
    edm = ""

    records = [
        lido_to_rdf(objid, x.text)
        for x in doc.findall(
            ".//{http://www.deutsche-digitale-bibliothek.de/ns/cortex-item-source}record"
        )
    ]
    return edm, records


def worker(number, Q):
    print(f"[green]{number}", end=" ")
    count = 0
    while True:
        objid, xml = Q.get()
        if objid is None:
            break

        try:
            edm, records = process(objid, xml)
        except:
            traceback.print_exc()
            continue

        # open(filepath_from(objid) + ".ttl", "w").write(edm)
        for idx, record in enumerate(records):
            subj, triples = record
            lido_rdf = "\n".join([f"{subj} {p} {o} ." for p, o in triples])
            lido_rdf = "\n" + lido_rdf
            open(os.path.join(OUTPUT_DIR, f"triples_{number}.nt"), "a").write(lido_rdf)

        count += 1
        if count % 99999 == 0:
            print(f"{number} {count}")


def main():
    INPUT_FILE = sys.argv[1]
    print(f"There are {multiprocessing.cpu_count()} CPUs")
    WORKER_COUNT = 90
    # There are 96 CPUs on teach02
    # Lets not use all of them, leave some free... ;-)

    Q = multiprocessing.Queue(1000)
    workers = []
    for w in range(WORKER_COUNT):
        wp = multiprocessing.Process(target=worker, daemon=True, args=(w, Q))
        wp.start()
        workers.append(wp)

    DB = sqlite3.connect(INPUT_FILE)
    cur = DB.cursor()
    cur.execute("SELECT count(id) FROM source")
    TOTAL_ITEMS = cur.fetchall()[0][0]
    print(f"In [green]{INPUT_FILE}[/green] are {TOTAL_ITEMS} items to process")

    cur.execute("SELECT * FROM source")
    count = 0
    started = time.time()
    timestamp = time.time()
    for objid, last_download, xml in cur:
        Q.put((objid, xml))
        count += 1
        if count % 9999 == 0:
            elapsed = int(time.time() - timestamp)
            if elapsed == 0:
                elapsed = 1
            timestamp = time.time()
            tps = 9999 / elapsed
            left_seconds = TOTAL_ITEMS / tps
            left_minutes = round(left_seconds / 60)
            left_hours = left_minutes / 60
            print(
                f"{time.ctime()} [green]{count}[/green] {tps} |{left_hours} hours|   |{left_minutes} min|"
            )
    for x in range(WORKER_COUNT):
        Q.put((None, None))
    for w in workers:
        w.join()


def test_one():
    class Q:
        def __init__(self, filename):
            DB = sqlite3.connect(filename)
            self.buf = [
                (objid, xml)
                for objid, last_download, xml in DB.execute(
                    "SELECT * FROM source LIMIT 9"
                )
            ]

        def get(self):
            if not self.buf:
                return None, None
            return self.buf.pop()

    worker(1, Q(sys.argv[1]))


if __name__ == "__main__":
    main()
