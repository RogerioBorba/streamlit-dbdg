import xml.etree.ElementTree as ET
from ..requests.request import get_xml
import time



class WFSDescribeFeatureType:
    def __init__(self, descricao: str, sigla: str, url: str) -> None:
        self.descricao = descricao
        self.sigla = sigla
        self.url = url
        self.tempo_requisicao: float = -1
        self.qtd_feicoes: int = -1
        self.xml: str | None = None
        self._root_xml: ET.Element | None = None

    async def execute_request(self)-> None:
        s = time.perf_counter()
        self.xml = await get_xml(self.url)
        elapsed = time.perf_counter() - s
        self.tempo_requisicao = round(elapsed, 2)
        #self.set_qtd_feicoes()
        
    def __str__(self) -> str:
        return self.descricao
    
    def __repr__(self) -> str:
        return self.descricao
    

    def root_xml(self) -> ET.Element:
        if self._root_xml == None:
            self._root_xml = ET.fromstring(self.xml)
        return self._root_xml