from rich.progress import track
import json, os, sys, httpx, traceback, random, io, hashlib
import xml.etree.ElementTree as ET
import pyoxigraph as px

"""
Where:
ns0="{http://www.openarchives.org/OAI/2.0/}"
ns1="{http://www.lido-schema.org}"
/ns0:record/ns0:metadata/ns1:lidoWrap/ns1: ... etc.

{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectClassificationWrap/{ns1}objectWorkTypeWrap/{ns1}objectWorkType/{ns1}conceptID"
https://nfdi4culture.de/ontology#objectWorkType

{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}titleWrap/{ns1}titleSet/{ns1}appellationValue"
http://schema.org/name

{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}repositoryWrap/{ns1}repositorySet/{ns1}repositoryName/{ns1}legalBodyID"
http://schema.org/publisher

{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectRelationWrap/{ns1}subjectWrap/{ns1}subjectSet/{ns1}subject/{ns1}subjectConcept/{ns1}conceptID"
http://schema.org/keywords

{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}objectDescriptionWrap/{ns1}objectDescriptionSet/{ns1}descriptiveNoteValue"
http://purl.org/dc/terms/description

The following needs to be combined in a bugfix specific to Heidelberg
{ns1}lido/{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordID"
{ns1}lido/{ns1}administrativeMetadata/{ns1}resourceWrap/{ns1}resourceSet/{ns1}resourceRepresentation/{ns1}linkResource"

lido:lido/lido:descriptiveMetadata/lido:objectIdentificationWrap/lido:repositoryWrap/lido:repositorySet/lido:workID
This is an inventory number

lido:lido/lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventMaterialsTech/lido:materialsTech/lido:termMaterialsTech/lido:conceptID
These are materials, are we bunging it into keywords as well? YES.

lido:lido/lido:descriptiveMetadata/lido:eventWrap/lido:eventSet/lido:event/lido:eventDate/lido:displayDate
some kind of date?
"""


def parse(filename):
    t = []
    ta = t.append

    ns1 = "{http://www.lido-schema.org}"
    _, f = os.path.split(filename)
    subj = f.replace("oai:heidicon.ub.uni-heidelberg.de:", "").replace(".xml", "")

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
    materials = doc.findall(
        f"{ns1}lido/{ns1}descriptiveMetadata/{ns1}eventWrap/{ns1}eventSet/{ns1}event/{ns1}eventMaterialsTech/{ns1}materialsTech/{ns1}termMaterialsTech/{ns1}conceptID"
    )
    # we are combining them all into the schema:keywords...
    subjects.extend(materials)

    mdate = doc.find(
        f"{ns1}lido/{ns1}descriptiveMetadata/{ns1}eventWrap/{ns1}eventSet/{ns1}event/{ns1}eventDate/{ns1}displayDate"
    )

    description = doc.find(
        f".//{ns1}lido/{ns1}descriptiveMetadata/{ns1}objectIdentificationWrap/{ns1}objectDescriptionWrap/{ns1}objectDescriptionSet/{ns1}descriptiveNoteValue"
    )
    rid = doc.find(
        f".//{ns1}lido/{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordID"
    )

    if objectWorkType is not None and objectWorkType.text:
        ta(
            (
                px.NamedNode("https://nfdi4culture.de/ontology#objectWorkType"),
                px.NamedNode(objectWorkType.text),
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
                    px.NamedNode(lb.text),
                )
            )
    for subject in subjects:
        if subject.text:
            ta(
                (
                    px.NamedNode("http://schema.org/keywords"),
                    px.NamedNode(subject.text),
                )
            )

    for recordInfoLink in doc.findall(
        f".//{ns1}lido/{ns1}administrativeMetadata/{ns1}recordWrap/{ns1}recordInfoSet/{ns1}recordInfoLink"
    ):
        ta((px.NamedNode("http://schema.org/url"), px.NamedNode(recordInfoLink.text)))

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
                px.NamedNode("http://schema.org/image"),
                px.NamedNode(l),
            )
        )
        ta(
            (
                px.NamedNode("https://nfdi4culture.de/ontology#theIIIF"),
                px.NamedNode(l.replace("full/full/0/default.jpg", "info.json")),
            )
        )
    # Add a link to the OAI-PMH interface for this record.
    gr = f"<https://heidicon.ub.uni-heidelberg.de/api/v1/plugin/base/oai/oai?verb=GetRecord&metadataPrefix=lido&identifier={f.replace('.xml', '')}>"
    ta((px.NamedNode("https://nfdi4culture.de/ontology#theOAI"), gr))

    if mdate is not None and mdate.text:
        ta(
            (
                px.NamedNode("http://purl.org/dc/elements/1.1/date"),
                px.Literal(mdate.text),
            )
        )

    return (
        px.NamedNode(
            f"https://nfdi4culture.de/id/ark:/60538/{hashlib.md5(subj.encode('utf8')).hexdigest()}"
        ),
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
