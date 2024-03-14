import xml.etree.ElementTree as ET
from ..requests.request import get_xml
import time
class CapabilitiesBase:
    def __init__(self, descricao: str, sigla: str, url: str) -> None:
        self.descricao = descricao
        self.sigla = sigla
        self.url = url
        self.tempo_requisicao: float = -1
        self.qtd_camadas: int = -1
        self.qtd_camadas_sem_metadados: int = -1
        self.qtd_camadas_sem_palavras_chaves: int = -1
        self.qtd_camadas_sem_resumo = -1
        self.xml: str | None = None
        self._root_xml: ET.Element | None = None
        self._schema_location: str | None = None
        self.failed = False

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
    
    def root_xml(self) -> ET.Element:
        if self._root_xml == None:
            self._root_xml = ET.fromstring(self.xml)
        return self._root_xml
    
    def prefix_tag(self, tag: str) -> str:
        if self.schema_location():
            return '{' + self.schema_location() + '}' + tag
        return tag
    
    def find_all(self, tag: str, element: ET.Element | None = None ) -> list:
        if element:
            return element.findall(tag)
        return self.root_xml().findall(tag)

    def find(self, tag: str, element: ET.Element | None = None) -> ET.Element:
        if element:
            return element.find(tag)    
        return self.root_xml().find(tag)
    
    async def execute_request(self)-> None:
        s = time.perf_counter()
        self.xml = await get_xml(self.url,ssl=False)
        #print(f"xml: {self.url}")
        elapsed = time.perf_counter() - s
        self.tempo_requisicao = round(elapsed, 2)
        self.set_qtd_camadas()
        self.set_qtd_camadas_sem_metadados()
        self.set_qtd_camadas_sem_palavras_chaves()
        self.set_qtd_camadas_sem_resumo()
        #print("root-xml")
        #print(self.root_xml().attrib.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'))
        #print(self.root_xml().findall('{http://www.opengis.net/ows}ServiceIdentification'))