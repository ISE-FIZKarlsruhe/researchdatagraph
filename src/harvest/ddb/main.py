import httpx, sys, os, logging, json
import multiprocessing as mp


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
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug logging requested from config env DEBUG")
else:
    logging.basicConfig()

WORKER_COUNT = env("WORKER_COUNT", False, int) or 4
OUTPATH = env("OUTPATH")
ORG_ID = env("ORG_ID")
MAX_COUNT = env("MAX_COUNT", False, int)


SEARCH_API = "https://api.deutsche-digitale-bibliothek.de/search/index/search/select?rows=9999999&fl=id&q=provider_id:"
RETRIEVE_URI = (
    "https://api.deutsche-digitale-bibliothek.de/items/__OBJECTID__/source/record"
)


def worker(number, Q):
    logging.debug(f"Worker: {number}")
    while True:
        objid = Q.get()
        if objid is None:
            break
        if os.path.exists(os.path.join(OUTPATH, objid)):
            continue
        r = httpx.get(RETRIEVE_URI.replace("__OBJECTID__", objid), timeout=120)
        if r.status_code == 200:
            open(os.path.join(OUTPATH, objid), "wb").write(r.content)


def main():
    if not os.path.exists(OUTPATH):
        logging.debug(f"Creating directory: {OUTPATH}")
        os.mkdir(OUTPATH)

    docids_path = os.path.join(OUTPATH, f"{ORG_ID}.json")
    if os.path.exists(docids_path):
        results = json.load(open(docids_path))
    else:
        r = httpx.get(SEARCH_API + ORG_ID, timeout=120)
        if r.status_code != 200:
            raise Exception(f"Search failure {r.status_code} {r.text()}")
        results = r.json()
        open(docids_path, "wb").write(r.content)
    docids = [doc["id"] for doc in results["response"]["docs"]]
    logging.debug(f"Found {len(docids)} documents")

    Q = mp.Queue(1000)
    workers = []
    for w in range(WORKER_COUNT):
        wp = mp.Process(target=worker, daemon=True, args=(w, Q))
        wp.start()
        workers.append(wp)

    count = 0
    for objid in docids:
        Q.put(objid)
        count += 1
        if MAX_COUNT and count >= MAX_COUNT:
            logging.debug(f"Count {count} is >= {MAX_COUNT}, stopping.")
            break

    for x in range(WORKER_COUNT):
        Q.put(None)

    for w in workers:
        w.join()
    logging.debug("Done: processed {count} exiting")


if __name__ == "__main__":
    main()
