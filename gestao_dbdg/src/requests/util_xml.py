import xml.etree.ElementTree as ET

def prefix_tag(tag: str, namespace: str = '') -> str:
        if namespace:
            return '{' + namespace + '}' + tag
        return tag

def find_all(tag: str, element: ET.Element)-> list:
        return element.findall(tag)

def find(tag: str, element: ET.Element) -> ET.Element | None:
        return element.find(tag)


def hits_csw_GetRecordsResponse(xml):
    namespaces = {
        'csw': 'http://www.opengis.net/cat/csw/2.0.2',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
    root = ET.fromstring(xml)

    # Encontrando os elementos necessários usando a função find() com o namespace
    search_results = root.find('csw:SearchResults', namespaces)
    matched = search_results.attrib.get('numberOfRecordsMatched')
    next_record = search_results.attrib.get('nextRecord')
    records_returned = search_results.attrib.get('numberOfRecordsReturned')
    return matched, records_returned, next_record
