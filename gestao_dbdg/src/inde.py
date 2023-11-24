from src.request import fetch_json
url = 'https://inde.gov.br/api/catalogo/get'
import json
from collections import namedtuple
catalogo_inde = []

catalogos_ibge = '''
[{
        "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - CGMAT",
        "sigla": "IBGE",
        "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
        "wmsAvailable": true,
        "wfsAvailable": true,
        "wcsAvailable": true,
        "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGMAT/ows?service=WMS&request=GetCapabilities",
        "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGMAT/ows?service=wfs&request=GetCapabilities&version=1.3.0",
        "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGMAT/ows?service=wcs&request=GetCapabilities&version=1.3.0",
        "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
        "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - CCAR",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CCAR/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CCAR/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CCAR/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - CGED",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGED/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGED/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGED/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - CGEO",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGEO/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGEO/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CGEO/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística  - CETE",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CETE/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CETE/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CETE/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - CMA",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CREN/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CREN/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/CREN/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - BDIA",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/BDIA/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/BDIA/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/BDIA/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        {
            "descricao": "IBGE - Instituto Brasileiro de Geografia e Estatística - PNADC",
            "sigla": "IBGE",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/PNADC/ows?service=WMS&request=GetCapabilities",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/PNADC/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/PNADC/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
        },
        
        {
            "descricao": "IBGE - Objetivos de Desenvolvimento Sustentável - ODS",
            "sigla": "IBGE/ODS",
            "url": "https://geoservicos.ibge.gov.br/geoserver/ODS/ows",
            "wmsAvailable": true,
            "wfsAvailable": true,
            "wcsAvailable": true,
            "wmsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/ODS/ows?service=wms&request=GetCapabilities&version=1.3.0",
            "wfsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/ODS/ows?service=wfs&request=GetCapabilities&version=1.3.0",
            "wcsGetCapabilities": "https://geoservicos.ibge.gov.br/geoserver/ODS/ows?service=wcs&request=GetCapabilities&version=1.3.0",
            "url_metadados": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge",
            "cswGetCapabilities": "https://metadadosgeo.ibge.gov.br/geonetwork_ibge/srv/por/csw?service=CSW&version=2.0.2&request=GetCapabilities"
            }
]'''
async def catalogos_dbdg()-> list[dict] | dict:
    try:
        catalogos : list = []
        catalogo_inde = await fetch_json(url)
        for catalogo in catalogo_inde:
            if catalogo['descricao'].startswith('IBGE -'):
                catalogos = catalogos + json.loads(catalogos_ibge)
            
            else:
                catalogos.append(catalogo)
        return  catalogos
    
    except Exception as exc:
        print(exc)
        return []

def descricao_sigla_url(dict_catalogo_inde: dict) -> namedtuple:
    descricao: str = dict_catalogo_inde['descricao']
    sigla: str = descricao[:descricao.find('-')].strip()
    url: str =  dict_catalogo_inde['wmsGetCapabilities']
    DescricaoSiglaUrl = namedtuple("DescricaoSiglaUrl", ["descricao", "sigla", "url"])
    return DescricaoSiglaUrl(descricao=descricao.strip(), sigla=sigla, url=url)

async def wms_capabilities() -> list[namedtuple]:
    if catalogo_inde:
        return [ dic['wmsGetCapabilities'] for dic in  catalogo_inde]
    list_dic = await catalogos_dbdg()
    return [ descricao_sigla_url(dic) for dic in list_dic]
