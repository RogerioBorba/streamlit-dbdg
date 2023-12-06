
import xml.etree.ElementTree as ET
from gestao_dbdg.src.requests.util_xml import  prefix_tag

class LegendURL:
    def __init__(self, element: ET.Element, namespace: str= '', ns_attribute='{http://www.w3.org/1999/xlink}') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self.ns_attribute = ns_attribute

class Style:
    def __init__(self, element: ET.Element, namespace: str= '', ns_attribute='{http://www.w3.org/1999/xlink}') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self.ns_attribute = ns_attribute
        self.ele_name: ET.Element = self.element.find(prefix_tag('Name', self.ns))
        self.ele_title: ET.Element = self.element.find(prefix_tag('Title', self.ns))
        self.ele_abstract: ET.Element = self.element.find(prefix_tag('Abstract', self.ns))
        self.ele_legend: ET.Element = self.element.find(prefix_tag('LegendURL', self.ns))

    def name(self) -> str | None:
        if self.ele_name is not None:
            return self.ele_name.text
        
    def simple_name(self) -> str | None:
        if self.name() is not None:
            names = self.name().split(':')
            return names[1] if len(names) > 1 else names[0]
        
    def title(self) -> str | None:
        if self.ele_title is not None:
            return self.ele_title.text
    
    def abstract(self) -> str | None:
        if self.ele_abstract is not None:
            return self.ele_abstract.text
        
class MetadataURL:
    def __init__(self, element: ET.Element, namespace: str= '', ns_attribute='{http://www.w3.org/1999/xlink}') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self.ns_attribute = ns_attribute
        self.attribute_type = self.element.get("type")
        self.ele_format: ET.Element = self.element.find(prefix_tag('Format', self.ns))
    
    def type(self) -> str:
        return self.attribute_type
    
    def format(self) -> str | None: 
        if self.ele_format is not None:
            return self.ele_format.text
    
    def url(self) -> str: 
        online_resource: ET.Element = self.element.find(prefix_tag('OnlineResource', self.ns))
        return online_resource.get(f"{self.ns_attribute}href")
    
class WMSLayer:
    def __init__(self, element: ET.Element, namespace: str= '') -> None:
        self.element: ET.Element = element
        self.ns = namespace
        self._title: ET.Element = element.find(prefix_tag('Title', self.ns))
        self._name: ET.Element = element.find(prefix_tag('Name', self.ns))
        self._abstract: ET.Element = element.find(prefix_tag('Abstract', self.ns))
        self.ele_metadata_list: list[ET.Element] = element.findall(prefix_tag('MetadataURL', self.ns))
        self.ele_keyword_list: ET.Element = element.find(prefix_tag('KeywordList', self.ns))
        self.ele_crs_list: list[ET.Element] = element.findall(prefix_tag('CRS', self.ns))
        self.ele_style: ET.Element = element.find(prefix_tag('Style', self.ns))
        self.style = Style(self.ele_style, self.ns) if self.ele_style is not None else None
        self.metadados_urls: list[MetadataURL] =  [ MetadataURL(ele, self.ns) for ele in self.ele_metadata_list]

    
    def name(self) -> str | None:
        if self._name is not None:
            return self._name.text
        
    def simple_name(self) -> str | None:
        if self.name() is not None:
            names = self.name().split(':')
            return names[1] if len(names) > 1 else names[0]
        
        
    def type(self) -> str:
        return 'Layer' if self.name() else 'LayerGroup'

    def palavras_chaves(self) -> list[str]:
        if self.ele_keyword_list:
            ele_list: list[ET.Element] = self.ele_keyword_list.findall(prefix_tag('Keyword', self.ns))
            return [ele.text for ele in ele_list]
        return []
    
    def url_metadado_links(self) -> list[str]:
    
        return [ metadata_url.url() for metadata_url in self.metadados_urls]

    def crss(self)-> list[str]:
        return [ ele_crs.text for ele_crs in self.ele_crs_list]
