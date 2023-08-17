import requests
import json
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
#from rdflib_jsonld.parser import Parser

url = "https://zenodo.org/api/records/4064862"
headers = {"Accept": "application/ld+json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("zenodo_record.json", "w") as file:
        file.write(response.text)
else:
    print("Failed to retrieve data.")

with open("zenodo_record.json", "r") as file:
    json_ld_data = json.load(file)

# Create an RDF graph
graph = Graph()

graph.parse(data=json.dumps(json_ld_data), format="json-ld")

# Serialize the graph to Turtle format and save to a file
with open("zenodo_record.ttl", "w", encoding="utf-8") as output_file:
    output_file.write(graph.serialize(format="turtle"))
