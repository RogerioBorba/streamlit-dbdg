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
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
            response = await client.get(url, headers=headers)
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
    

async def get_xml(url: str, ssl: bool = True):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl)) as session:

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
            #client_timeout = aiohttp.ClientTimeout(connect=5, sock_read=60)
            async with session.get(url, headers=headers, timeout=60) as resp:
                text = await resp.text()
                print(f"url: {url}")
                print(f"status: {resp.status}")
               # print(text )
                return text
            