import requests

# URL del endpoint de envío
URL = "https://chl-b2950867-d414-493e-95b1-36983c31e1c6-aldeas-inseguras-v2.softwareseguro.com.ar/src/ctl/enviar_mercancia.ctl.php"

# Cookie de sesión
PHPSID = "ddbfb833f2db28dd1832d2fc703db9c9" # Cambia esto por tu PHPSESSID

# Cadena de jugadores (puede incluir más)
jugadores = [
    {"nombre": "Andrés", "id": "39bffa01f5b07b2a651fe9d973492e46",
        "oro": 0, "plata": 1162, "bronce": 9752},
    {"nombre": "Valeria", "id": "111ccefe3a4a88fbf9a7260547dbc084",
        "oro": 4563, "plata": 2022, "bronce": 2453},
    {"nombre": "Iván", "id": "bc4aa16b743a3dfba7b9617b8fcca2a3",
        "oro": 4552, "plata": 1543, "bronce": 4340},
    {"nombre": "Benjamín", "id": "74d2afa3a1f4894c8829c6f80a7a436b",
        "oro": 4415, "plata": 125, "bronce": 3177},
    {"nombre": "Felipe", "id": "9fedb91a0f93706d7f09b44d0e5b94c1",
        "oro": 4676, "plata": 3489, "bronce": 8519},
    {"nombre": "Gabriela", "id": "d68e1ad7131220df462d00caf7d52001",
        "oro": 4029, "plata": 2600, "bronce": 10148},
    {"nombre": "Sofía", "id": "8531995b7030121c4440299ffefd65ef",
        "oro": 4910, "plata": 1631, "bronce": 2058},
    {"nombre": "Fabricio", "id": "20775e3bb85fa3ec2701d374057540de",
        "oro": 4439, "plata": 3257, "bronce": 9305},
    {"nombre": "Elena", "id": "f29ae2207b53b27bc0cfb758b910476f",
        "oro": 4018, "plata": 1739, "bronce": 14388},
    {"nombre": "Ezequiel", "id": "ef098d1695add0b35b5c65b3827ad3b4",
        "oro": 0, "plata": 3493, "bronce": 0},
    {"nombre": "Cecilia", "id": "96f6667851fab55af355753e9d806cf3",
        "oro": 0, "plata": 3387, "bronce": 0},
    {"nombre": "Ramiro", "id": "bde44e88ebd3925ff843b2e31bda83d7",
        "oro": 0, "plata": 3344, "bronce": 0},
    {"nombre": "Julieta", "id": "40dd93cfc62726d9a10e378d63fe9fb2",
        "oro": 0, "plata": 3344, "bronce": 0},
    {"nombre": "Tomás", "id": "ef257c0254b32357433c5d0dd5388522",
        "oro": 0, "plata": 3313, "bronce": 0},
    {"nombre": "Lautaro", "id": "4a868daa1f4aa72e01b10e6fee6c736d",
        "oro": 0, "plata": 3288, "bronce": 0},
    {"nombre": "Sebastián", "id": "ce04175308c38ebe1429f866c2480b57",
        "oro": 0, "plata": 3207, "bronce": 0},
    {
        "nombre": "Pedro", # Jugador de la aldea
        "id": "bdbcc9b006186e87657912bbb0411a37",
        "oro": 0,
        "plata": 0,
        "bronce": 0,
    },
]# al ser el ultimo jugador, todo lo acumulado se le enviara a el

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
}

cookies = {
    "PHPSESSID": PHPSID,
}


def enviar_recurso(jugadores, tipo_recurso):
    nombre_recurso = {1: "Oro", 2: "Plata", 3: "Bronce"}[tipo_recurso]
    print(f"\n🛒 Enviando {nombre_recurso} en cadena...\n")

    for i in range(len(jugadores) - 1):
        origen = jugadores[i]
        destino = jugadores[i + 1]

        cantidad = sum(jugadores[j][["oro", "plata", "bronce"]
                       [tipo_recurso - 1]] for j in range(i + 1))

        data = {
            "id_jugador_origen": origen["id"],
            "select_jugador_destino": destino["id"],
            "select_recurso": str(tipo_recurso),
            "txt_cantidad": str(cantidad),
        }

        print(
            f"🔁 {origen['nombre']} → {destino['nombre']} | {nombre_recurso}: {cantidad}")
        response = requests.post(URL, headers=headers,
                                 cookies=cookies, data=data)

        print(f"📦 Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Envío exitoso.")
        else:
            print("⛔ Error en el envío.")
        print("-" * 40)


enviar_recurso(jugadores, tipo_recurso=1)  # Oro
enviar_recurso(jugadores, tipo_recurso=2)  # Plata
enviar_recurso(jugadores, tipo_recurso=3)  # Bronce
