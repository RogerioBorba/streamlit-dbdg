import xml.etree.ElementTree as ET
from ..requests.request import get_xml
import time
from gestao_dbdg.src.wfs.wfs_layer import WFSLayer
from gestao_dbdg.src.capabilities.capabililties_base import CapabilitiesBase

class WFSCapabilities(CapabilitiesBase):
    def __init__(self, descricao: str, sigla: str, url: str) -> None:
        super().__init__(descricao, sigla, url)
        self.is_layer_group: bool = False
        self._elements: list[ET.Element] | None = None
    
    
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

    
    def ele_FeatureTypeList(self) -> ET.Element:
        return self.find(self.prefix_tag('FeatureTypeList'))
    
    def list_ele_FeatureType(self) -> list[ET.Element]:
        return self.ele_FeatureTypeList().findall(self.prefix_tag('FeatureType'))
    
    def layers(self) -> list[WFSLayer]:
        list_ft: list[ET.Element] = self.list_ele_FeatureType()

        return [ WFSLayer(ele_layer, self.schema_location()) for ele_layer in list_ft ]

    def set_qtd_camadas(self)-> None:
        self.qtd_camadas = len(self.layers())

    def set_qtd_camadas_sem_metadados(self)-> None:
        ele_layers: list[ET.Element] = self.list_ele_FeatureType()
        ele_layers = [ ele_layer for ele_layer in ele_layers if ele_layer.find(self.prefix_tag('MetadataURL')) == None]
        self.qtd_camadas_sem_metadados = len(ele_layers)
            
    def set_qtd_camadas_sem_resumo(self)-> None:
        ele_layers: list[ET.Element] = self.list_ele_FeatureType()
        #ele_layers = [ ele_layer for ele_layer in ele_layers if not (ele_layer.find(self.prefix_tag('Abstract')) != None and ele_layer.find(self.prefix_tag('Abstract')).text != '') ]
        qt_sem_resumo = 0
        for ele_layer in ele_layers:
            ele = ele_layer.find(self.prefix_tag('Abstract'))
            if  not (ele is not None and ele.text is not None):
                qt_sem_resumo += 1

        self.qtd_camadas_sem_resumo = qt_sem_resumo #len(ele_layers)
        

    def set_qtd_camadas_sem_palavras_chaves(self)-> None:
        ele_layers: list[ET.Element] = self.list_ele_FeatureType()
        count: int = 0
        for ele_layer in ele_layers:
            ele_KeywordList: ET.Element | None =  ele_layer.find('{http://www.opengis.net/ows}Keywords')
            if ele_KeywordList and len(ele_KeywordList.findall('{http://www.opengis.net/ows}Keyword')) > 0:
                count = count 
            else:
                count += 1
        self.qtd_camadas_sem_palavras_chaves = count
    
    