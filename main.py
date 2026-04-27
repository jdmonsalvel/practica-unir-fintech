"""API de clima usando Open-Meteo (sin API key requerida)."""
import httpx
from fastapi import FastAPI, HTTPException, Query
from typing import Optional

app = FastAPI(
    title="FinTech Weather API",
    description="API pública de información meteorológica para FinTech Solutions S.A.",
    version="1.0.0",
)

BASE_URL = "https://api.open-meteo.com/v1"

WMO_CODES: dict[int, str] = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna densa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia intensa",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada intensa",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    95: "Tormenta",
    99: "Tormenta con granizo",
}


@app.get("/")
def root() -> dict:
    return {"mensaje": "API de clima activa", "version": "1.0.0"}


@app.get("/clima/actual")
def clima_actual(
    latitud: float = Query(..., description="Latitud geográfica", ge=-90, le=90),
    longitud: float = Query(..., description="Longitud geográfica", ge=-180, le=180),
) -> dict:
    """Retorna el clima actual para las coordenadas dadas."""
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weathercode",
        "timezone": "auto",
    }
    response = httpx.get(f"{BASE_URL}/forecast", params=params, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error al consultar servicio de clima")

    data = response.json()
    current = data.get("current", {})
    codigo = current.get("weathercode", -1)

    return {
        "latitud": latitud,
        "longitud": longitud,
        "temperatura_c": current.get("temperature_2m"),
        "humedad_pct": current.get("relative_humidity_2m"),
        "viento_kmh": current.get("wind_speed_10m"),
        "condicion": WMO_CODES.get(codigo, "Desconocido"),
        "hora": current.get("time"),
        "zona_horaria": data.get("timezone"),
    }


@app.get("/clima/pronostico")
def pronostico(
    latitud: float = Query(..., ge=-90, le=90),
    longitud: float = Query(..., ge=-180, le=180),
    dias: int = Query(default=3, ge=1, le=7, description="Días de pronóstico (1-7)"),
) -> dict:
    """Retorna el pronóstico diario de temperatura máxima y mínima."""
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "auto",
        "forecast_days": dias,
    }
    response = httpx.get(f"{BASE_URL}/forecast", params=params, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error al consultar servicio de clima")

    data = response.json()
    daily = data.get("daily", {})
    fechas = daily.get("time", [])
    tmax = daily.get("temperature_2m_max", [])
    tmin = daily.get("temperature_2m_min", [])
    codigos = daily.get("weathercode", [])

    pronostico_list = [
        {
            "fecha": fechas[i],
            "temp_max_c": tmax[i],
            "temp_min_c": tmin[i],
            "condicion": WMO_CODES.get(codigos[i], "Desconocido"),
        }
        for i in range(len(fechas))
    ]

    return {
        "latitud": latitud,
        "longitud": longitud,
        "zona_horaria": data.get("timezone"),
        "pronostico": pronostico_list,
    }
