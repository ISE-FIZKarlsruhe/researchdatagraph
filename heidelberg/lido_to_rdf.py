from rich.progress import track
import json, os, sys, httpx, traceback, random, io, hashlib
import xml.etree.ElementTree as ET
import pyoxigraph as px


def parse(filename):
    t = []
    ta = t.append

    ns1 = "{http://www.lido-schema.org}"
    _, f = os.path.split(filename)
    subj = f.replace("oai:heidicon.ub.uni-heidelberg.de:", "").replace(".xml", "")

    ta((px.NamedNode("http://ise/oaiID"), px.Literal(f.replace(".xml", ""))))

    doc = ET.parse(filename)
    category = doc.find(f".//{ns1}lido/{ns1}category/{ns1}conceptID")
    objectWorkType = doc.find(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectClassificationWrap/{ns1}objectWorkTypeWrap/{ns1}objectWorkType/{ns1}conceptID"
    )
    title = doc.find(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}titleWrap/{ns1}titleSet/{ns1}appellationValue"
    )
    legalBody = doc.findall(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}repositoryWrap/{ns1}repositorySet/{ns1}repositoryName/{ns1}legalBodyID"
    )
    subjects = doc.findall(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectRelationWrap/{ns1}subjectWrap/{ns1}subjectSet/{ns1}subject/{ns1}subjectConcept/{ns1}conceptID"
    )
    description = doc.find(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}objectDescriptionWrap/{ns1}objectDescriptionSet/{ns1}descriptiveNoteValue"
    )
    rid = doc.find(
        f".//{ns1}lido/{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordID"
    )

    if category is not None and category.text:
        ta((px.NamedNode("http://ise/category"), px.NamedNode(category.text)))

    if objectWorkType is not None and objectWorkType.text:
        ta(
            (
                px.NamedNode("http://ise/objectWorkType"),
                px.NamedNode(objectWorkType.text),
            )
        )
    if title is not None and title.text:
        ta(
            (
                px.NamedNode("http://www.w3.org/2000/01/rdf-schema#Label"),
                px.Literal(title.text),
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
                    px.NamedNode("http://ise/CorporateBody"),
                    px.NamedNode(lb.text),
                )
            )
    for subject in subjects:
        if subject.text:
            ta((px.NamedNode("http://ise/keyword"), px.NamedNode(subject.text)))

    lids = doc.findall(
        f".//{ns1}lido/{ns1}administrativeMetadata/{ns1}resourceWrap/{ns1}resourceSet/{ns1}resourceRepresentation/{ns1}linkResource"
    )
    lids = [
        l.text.replace(
            "https://heidicon.ub.uni-heidelberg.de/iiif/2/%3A", f"{rid.text}:"
        )
        for l in lids
        if l.attrib.get("{http://www.lido-schema.org}label")
        == "IIIF Image API Base URI"
    ]
    lids = [
        f"https://heidicon.ub.uni-heidelberg.de/iiif/2/{l}/full/full/0/default.jpg"
        for l in lids
    ]
    for l in lids:
        ta(
            (
                px.NamedNode("http://www.europeana.eu/schemas/edm/isShownBy"),
                px.NamedNode(l),
            )
        )
        ta(
            (
                px.NamedNode("http://ise/theIIIF"),
                px.NamedNode(l.replace("full/full/0/default.jpg", "info.json")),
            )
        )
    # Add a link to the OAI-PMH interface for this record.
    gr = f"<https://heidicon.ub.uni-heidelberg.de/api/v1/plugin/base/oai/oai?verb=GetRecord&metadataPrefix=lido&identifier={f.replace('.xml', '')}>"
    ta((px.NamedNode("http://ise/theOAI"), gr))
    return (
        px.NamedNode(f"http://ise/{hashlib.md5(subj.encode('utf8')).hexdigest()}"),
        t,
    )


def main():
    LOC = sys.argv[1]
    files = [
        os.path.join(LOC, f)
        for f in os.listdir(LOC)
        if f.startswith("oai:heidicon.ub.uni-heidelberg.de:")
    ]
    for file in track(files):
        subj, triples = parse(file)
        for p, o in triples:
            print(f"{subj} {p} {o} .")


if __name__ == "__main__":
    main()
