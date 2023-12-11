import xml.etree.ElementTree as ET
from gestao_dbdg.src.requests.util_xml import  prefix_tag

class OWSBaseLayer:
    def __init__(self, element: ET.Element, namespace: str= '') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self._title: ET.Element = element.find(prefix_tag('Title', self.ns))
        self._name: ET.Element = element.find(prefix_tag('Name', self.ns))
        self._abstract: ET.Element = element.find(prefix_tag('Abstract', self.ns))
        self.ele_metadata_list: list[ET.Element] = element.findall(prefix_tag('MetadataURL', self.ns))
        self.ele_keyword_list: ET.Element = element.find(prefix_tag('KeywordList', self.ns))
        
    def name(self) -> str | None:
        if self._name is not None:
            return self._name.text
        
    def simple_name(self) -> str | None:
        if self.name() is not None:
            names = self.name().split(':')
            return names[1] if len(names) > 1 else names[0]
    
    def title(self) -> str | None:
        if self._title is not None:
            return self._title.text
        
    def abstract(self) -> str | None:
        if self._abstract is not None:
            return self._abstract.text
    