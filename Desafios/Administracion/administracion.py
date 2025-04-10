import base64
import json
from collections import defaultdict

# Ruta del archivo de tokens
file_path = "tokens.txt"

# Leer tokens desde el archivo
with open(file_path, "r") as f:
    tokens = [line.strip() for line in f if line.strip()]

# Diccionario para agrupar por `azp`
azp_groups = defaultdict(list)

# Procesar cada token
for token in tokens:
    parts = token.split(".")
    if len(parts) != 3:
        continue  # Token mal formado

    _, payload_b64, _ = parts
    padded_payload = payload_b64 + "=" * (-len(payload_b64) % 4)

    try:
        payload_json = base64.urlsafe_b64decode(padded_payload).decode("utf-8")
        payload = json.loads(payload_json)

        # Filtrar tokens firmados por Google
        if payload.get("iss") == "https://accounts.google.com":
            azp = payload.get("azp")
            email = payload.get("email")
            if azp and email:
                azp_groups[azp].append(email)

    except Exception as e:
        continue  # Saltar tokens inválidos

# Buscar grupos con exactamente 3 correos
for azp, emails in azp_groups.items():
    if len(emails) == 3:
        emails_sorted = sorted(emails)
        print("AZP sospechoso:", azp)
        print("Correos:", '|'.join(emails_sorted))
        break
