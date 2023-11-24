import xml.etree.ElementTree as ET
from .request import fetch_xml, get_xml
import time
from src.wms_layer import WMSLayer

class WMSCapabilities:
    def __init__(self, descricao: str, sigla: str, url: str) -> None:
        self.descricao = descricao
        self.sigla = sigla
        self.url = url
        self.tempo_requisicao: float = -1
        self.qtd_camadas: int = -1
        self.qtd_camadas_sem_metadados: int = -1
        self.qtd_camadas_sem_palavras_chaves: int = -1
        self.xml: str | None = None
        self._root_xml: ET.Element | None = None
        self._schema_location: str | None = None
        self.is_layer_group: bool = False
        self.failed = False
        self._elements_from_tree: list[ET.Element] | None = None
    
    def __str__(self) -> str:
        return self.descricao
    
    def __repr__(self) -> str:
        return self.descricao
    
    
    def version(self)-> str: 
         root: ET.Element = self.root_xml()
         return root.attrib.get('version')

    def schema_location(self)-> str:
        if self._schema_location is None:
            root: ET.Element = self.root_xml()
            string: str = root.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
            if string:
                self._schema_location = string.split(' ')[0].strip()
        return self._schema_location

    def prefix_tag(self, tag: str) -> str:
        if self.schema_location():
            return '{' + self.schema_location() + '}' + tag
        return tag
    
    def root_xml(self) -> ET.Element:
        if self._root_xml == None:
            self._root_xml = ET.fromstring(self.xml)
        return self._root_xml
    
    def find_all(self, tag: str, element: ET.Element | None = None ) -> list:
        if element:
            return element.findall(tag)
        return self.root_xml().findall(tag)

    def find(self, tag: str, element: ET.Element | None = None) -> ET.Element:
        if element:
            return element.find(tag)    
        return self.root_xml().find(tag)
    
    def ele_capability(self)-> ET.Element:
        return self.find(self.prefix_tag('Capability'))
    
    def ele_outer_layer(self)-> ET.Element:
        return  self.ele_capability().find(self.prefix_tag('Layer'))
    
    
    def ele_layer_has_name(self, ele_layer: ET.Element) -> bool:
        tag_name: str = self.prefix_tag('Name')
        return self.find(tag_name, ele_layer) is not None
    
    def elements_tree_layer(self, ele_layer: ET.Element) -> list:
        
        list_ele_layers: list[ET.Element] = []
        prefixed_tag = self.prefix_tag('Layer')
        if self.ele_layer_has_name(ele_layer):
            list_ele_layers.append(ele_layer)
        children_elements = self.find_all(prefixed_tag, ele_layer)
        for ele in children_elements:
            list_ele_layers = list_ele_layers + self.elements_tree_layer(ele)
        
        return list_ele_layers
   
    def layers_from_tree(self)-> list:
        ele = self.ele_outer_layer()
        if ele:
            return self.elements_tree_layer(ele)
        return []

    def wms_layers(self) -> list[WMSLayer]:
        return [ WMSLayer(ele_layer, self.schema_location()) for ele_layer in self.layers_from_tree()]

    def set_qtd_camadas(self)-> None:
        res: ET.Element = self.ele_capability().find(self.prefix_tag('Layer'))
        self.qtd_camadas = len(self.layers_from_tree())

    def set_qtd_camadas_sem_metadados(self)-> None:
        res: ET.Element = self.ele_capability().find(self.prefix_tag('Layer'))
        ele_layers: list = self.layers_from_tree()
        ele_layers = [ ele_layer for ele_layer in ele_layers if ele_layer.find(self.prefix_tag('MetadataURL')) == None]
        self.qtd_camadas_sem_metadados = len(ele_layers)
            
    def set_qtd_camadas_sem_palavras_chaves(self)-> None:
        res: ET.Element = self.ele_capability().find(self.prefix_tag('Layer'))
        ele_layers: list = self.layers_from_tree()
        count: int = 0
        for ele_layer in ele_layers:
            ele_KeywordList: ET.Element | None =  ele_layer.find(self.prefix_tag('KeywordList')) 
            if ele_KeywordList and len(ele_KeywordList.findall(self.prefix_tag('Keyword'))) > 0:
                count = count 
            else:
                count += 1
        self.qtd_camadas_sem_palavras_chaves = count
    
    async def execute_request(self)-> None:
        s = time.perf_counter()
        self.xml = await get_xml(self.url)
        elapsed = time.perf_counter() - s
        self.tempo_requisicao = round(elapsed, 2)
        self.set_qtd_camadas()
        self.set_qtd_camadas_sem_metadados()
        self.set_qtd_camadas_sem_palavras_chaves()
