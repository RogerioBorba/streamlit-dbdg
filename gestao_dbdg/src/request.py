import httpx
import requests
import ssl
import aiohttp

async def fetch_json(url) -> dict:
    context = ssl._create_unverified_context()
    verify: bool = False if url == 'https://inde.gov.br/api/catalogo/get'else True
    async with httpx.AsyncClient(verify=verify) as client:
        response = await client.get(url)
        return response.json()
    
async def fetch_xml(url) -> str:
    #verify: bool = False if url == 'https://inde.gov.br/api/catalogo/get'else True
    async with httpx.AsyncClient(verify=False) as client:
        try:
            print(url)
            response = await client.get(url)
            print(response.status_code)
            print(f"response.text: {len(response.text)}")
            #if response.status_code == 301:
            #    return requests.get(url).text
            return response.text
        except TimeoutError:
                #print(response)
                print(f"timeout na url: {url} ")
        except Exception as exc:
                print(exc)
                print(f"Erro na requisição: {url} ")
    

async def get_xml(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                #print(resp.status)
                text = await resp.text()
               # print(text )
                return text
            