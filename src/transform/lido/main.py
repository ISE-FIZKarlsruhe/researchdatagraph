import multiprocessing, sys, os, logging, time
from datetime import datetime
import pyoxigraph as px
import xxhash
import lidolator


def env(key, mandatory=True, coercion=str):
    tmp = os.environ.get(key)
    if mandatory and tmp is None:
        logging.exception(f"Environment variable {key} not defined")
        sys.exit(1)
    if tmp is not None:
        return coercion(tmp)
    return tmp


DEBUG = env("DEBUG", False) == "1"
if DEBUG:
    DEBUG = logging.DEBUG
else:
    DEBUG = logging.INFO
logging.basicConfig(level=DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

OUTPATH = env("OUTPATH")
INPATH = env("INPATH")
MAX_COUNT = env("MAX_COUNT", False, int)
PUBLISHER_IRI = env("PUBLISHER_IRI")
OBJID_PREFIX = env("OUTPATH", False) or ""
SOURCE_URI_TEMPLATE = env("SOURCE_URI_TEMPLATE")


def NN(val):
    try:
        return px.NamedNode(val)
    except:
        return px.Literal(val)


def process(filepath):
    _, filename = os.path.split(filepath)
    objid = filename.replace(".xml", "")

    t = []
    ta = t.append

    doc = lidolator.from_file(filepath)
    ns1 = "{http://www.lido-schema.org}"

    subj = f"{OBJID_PREFIX}{objid}"

    # As the first version of proving the PID theory, use xxhash of the URI here!
    subj_hash = xxhash.xxh64(f"<{subj}>").intdigest()
    subj_uri = px.NamedNode(f"https://nfdi.fiz-karlsruhe.de/id/ark:/60538/{subj_hash}")

    ta(
        (
            subj_uri,
            px.NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            px.NamedNode("https://nfdi.fiz-karlsruhe.de/ontology/Item"),
        )
    )
    ta(
        (
            subj_uri,
            px.NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            px.NamedNode("https://schema.org/CreativeWork"),
        )
    )

    ta(
        (
            subj_uri,
            px.NamedNode("http://schema.org/publisher"),
            px.NamedNode(PUBLISHER_IRI),
        )
    )

    ta(
        (
            subj_uri,
            px.NamedNode("http://purl.org/dc/terms/source"),
            px.NamedNode(SOURCE_URI_TEMPLATE.replace("__objid__", objid)),
        )
    )

    fields_to_properties_namednodes = {
        "recordInfoLink": "http://schema.org/url",
        "image": "http://schema.org/image",
        "objectWorkType": "http://schema.org/keywords",
        "classification": "http://schema.org/keywords",
        "location": "https://nfdi.fiz-karlsruhe.de/ontology/location",
        "legalBody": "http://schema.org/publisher",
        "subjects": "http://schema.org/keywords",
        "materials": "http://schema.org/keywords",
        "actor": "https://nfdi.fiz-karlsruhe.de/ontology/person_organization",
    }

    for field, property in fields_to_properties_namednodes.items():
        for val in doc.get(field, []):
            if val.text:
                ta((subj_uri, px.NamedNode(property), NN(val.text)))

    fields_to_properties_literals = {
        "title": "http://schema.org/name",
        "description": "http://schema.org/description",
        "displayDate": "http://purl.org/dc/terms/date",
        "earliestDate": (
            "https://nfdi.fiz-karlsruhe.de/ontology/earliestDate",
            "http://www.w3.org/2001/XMLSchema#gYear",
        ),
        "latestDate": (
            "https://nfdi.fiz-karlsruhe.de/ontology/latestDate",
            "http://www.w3.org/2001/XMLSchema#gYear",
        ),
        "place": "http://purl.org/dc/elements/1.1/coverage",
    }

    for field, property in fields_to_properties_literals.items():
        datatype = None
        if type(property) is tuple:
            property, datatype = property
        for val in doc.get(field, []):
            if val.text:
                if datatype:
                    ta(
                        (
                            subj_uri,
                            px.NamedNode(property),
                            px.Literal(val.text, datatype=px.NamedNode(datatype)),
                        )
                    )
                else:
                    language = val.attrib.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    )
                    if language:
                        ta(
                            (
                                subj_uri,
                                px.NamedNode(property),
                                px.Literal(val.text, language=language),
                            )
                        )
                    else:
                        ta((subj_uri, px.NamedNode(property), px.Literal(val.text)))

    return t


def worker(number, Q):
    count = 0
    while True:
        obj = Q.get()
        if obj is None:
            break
        try:
            records = process(obj)
        except:
            logging.exception(f"Problem with {obj}")
            continue

        with open(os.path.join(OUTPATH, f"worker_{number}.nt"), "a") as F:
            F.write("\n".join([f"{s} {p} {o} ." for s, p, o in records]))
            F.write("\n")

        count += 1
        if count % 99999 == 0:
            logging.debug(f"{number} {count}")


def main():
    if not os.path.exists(OUTPATH):
        logging.debug(f"Creating directory: {OUTPATH}")
        os.mkdir(OUTPATH)

    start_time = time.time()
    cpu_count = multiprocessing.cpu_count()
    WORKER_COUNT = cpu_count - 3
    logging.debug(f"There are {cpu_count} CPUs, using {WORKER_COUNT}")

    Q = multiprocessing.Queue(1000)
    workers = []
    for w in range(WORKER_COUNT):
        wp = multiprocessing.Process(target=worker, daemon=True, args=(w, Q))
        wp.start()
        workers.append(wp)

    count = 0
    for filename in os.listdir(INPATH):
        Q.put(os.path.join(INPATH, filename))
        count += 1
        if MAX_COUNT and count >= MAX_COUNT:
            logging.debug(f"Count {count} is >= {MAX_COUNT}, stopping.")
            break

    for w in range(WORKER_COUNT):
        Q.put(None)
    for w in workers:
        w.join()

    with open(os.path.join(OUTPATH, "out.nt"), "w") as F:
        for worker_file in os.listdir(OUTPATH):
            if worker_file.startswith("worker_") and worker_file.endswith(".nt"):
                worker_file_path = os.path.join(OUTPATH, worker_file)
                F.write(open(worker_file_path).read())
                os.unlink(worker_file_path)

    end_time = time.time()
    logging.debug(f"Duration: {int(end_time-start_time)} seconds")


if __name__ == "__main__":
    main()
