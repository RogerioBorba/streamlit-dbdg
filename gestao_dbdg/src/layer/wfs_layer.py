import xml.etree.ElementTree as ET
from gestao_dbdg.src.requests.util_xml import  prefix_tag
from gestao_dbdg.src.layer.base_layer import OWSBaseLayer
from collections import namedtuple
MetadataUrl = namedtuple("MetadataUrl", ["type", "url", "format"])
class WFSLayer(OWSBaseLayer):
    def __init__(self, element: ET.Element, namespace: str= '') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self._title: ET.Element = element.find(prefix_tag('Title', self.ns))
        self._name: ET.Element = element.find(prefix_tag('Name', self.ns))
        self._abstract: ET.Element = element.find(prefix_tag('Abstract', self.ns))
        self.ele_metadata_list: list[ET.Element] = element.findall(prefix_tag('MetadataURL', self.ns))
        self.ele_keyword_list: ET.Element = element.find('{http://www.opengis.net/ows}Keywords')
        #print(element)
        #print(self.ele_keyword_list)
        self.ele_crs_list: list[ET.Element] = element.findall(prefix_tag('DefaultSRS', self.ns))
        self.metadados_urls: list[MetadataUrl] =  [ MetadataUrl(ele.get("type"), ele.text, ele.get("format")) for ele in self.ele_metadata_list]

    def name(self) -> str | None:
        
        if self._name is not None:
            return self._name.text


    def palavras_chaves(self) -> list[str]:
        if self.ele_keyword_list:
            ele_list: list[ET.Element] = self.ele_keyword_list.findall('{http://www.opengis.net/ows}Keyword')
            return [ele.text for ele in ele_list]
        return []
    
    def crss(self)-> list[str]:
        return [ ele_crs.text for ele_crs in self.ele_crs_list]