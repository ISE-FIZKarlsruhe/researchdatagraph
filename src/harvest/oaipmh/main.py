import httpx, os, logging, sys
import xml.etree.ElementTree as ET


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


OUTPATH = env("OUTPATH")
URI = env("URI")
METADATA = env("METADATA")
MAX_COUNT = env("MAX_COUNT", False, int)


def parse(result: str):
    doc = ET.fromstring(result)
    buf = doc.findall(".//{http://www.openarchives.org/OAI/2.0/}record")
    token = doc.find(".//{http://www.openarchives.org/OAI/2.0/}resumptionToken")
    if token is not None:
        token = token.text
    return buf, token


def main():
    if not os.path.exists(OUTPATH):
        logging.debug(f"Creating directory: {OUTPATH}")
        os.mkdir(OUTPATH)
    r = httpx.get(f"{URI}?verb=ListRecords&metadataPrefix={METADATA}", timeout=120)
    if r.status_code != 200:
        raise Exception(f"{r.text} {r.status_code}")
    buf, token = parse(r.text)
    count = 0
    while token:
        for record in buf:
            i = record.find(".//{http://www.openarchives.org/OAI/2.0/}identifier").text
            open(os.path.join(OUTPATH, i), "wb").write(ET.tostring(record))
            count += 1
            if MAX_COUNT and count >= MAX_COUNT:
                logging.debug(f"Count {count} is >= {MAX_COUNT}, stopping.")
                token = None
                break
        r = httpx.get(f"{URI}?verb=ListRecords&resumptionToken={token}", timeout=60)
        if r.status_code != 200:
            raise Exception(f"{r.text} {r.status_code}")
        buf, token = parse(r.text)
    logging.info(f"Done with {URI} {METADATA} in {OUTPATH}")


if __name__ == "__main__":
    main()
