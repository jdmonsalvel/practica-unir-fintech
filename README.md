# FinTech Weather API

API REST de información meteorológica pública basada en [Open-Meteo](https://open-meteo.com/). No requiere API key.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado de la API |
| GET | `/clima/actual` | Clima actual por coordenadas |
| GET | `/clima/pronostico` | Pronóstico diario (1-7 días) |

## Uso rápido

```bash
# Instalar dependencias
make install

# Ejecutar localmente
make run
```

```bash
# Clima actual en Madrid (40.4168, -3.7038)
curl "http://localhost:8000/clima/actual?latitud=40.4168&longitud=-3.7038"

# Pronóstico 5 días en Bogotá (4.7110, -74.0721)
curl "http://localhost:8000/clima/pronostico?latitud=4.7110&longitud=-74.0721&dias=5"
```

## Documentación interactiva

Con la app corriendo, accede a `http://localhost:8000/docs`

## Estructura

```
.
├── main.py          # Aplicación FastAPI
├── requirements.txt
├── Makefile
└── Dockerfile
```
