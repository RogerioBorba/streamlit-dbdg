import xml.etree.ElementTree as ET

def prefix_tag(tag: str, namespace: str = '') -> str:
        if namespace:
            return '{' + namespace + '}' + tag
        return tag

def find_all(tag: str, element: ET.Element)-> list:
        return element.findall(tag)

def find(tag: str, element: ET.Element) -> ET.Element | None:
        return element.find(tag)    