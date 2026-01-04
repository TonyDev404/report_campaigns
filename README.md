# Ejecutable: Reporte de Campañas

Herramienta interna para generar reportes de campañas (DIGITAL / DIALER) en formato Excel mediante una interfaz web.

## Estructura

- `Backend/` -> API FastAPI
- `Frontend/` -> UI Svelte + Vite

## Desarrollo local

### Backend (Windows)
```powershell
cd Backend
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

El backend estará disponible en: http://localhost:8000

### Frontend
```
cd Frontend
npm install
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## Variables de entorno
Copiar el archivo de ejemplo y completar los valores:
```
Backend/envexample -> Backend/.env
```

## Build

### Frontend
```
cd Frontend
npm run build
```

### Backend
Para generar un ejecutable (opcional) usando PyInstaller:
```
cd Backend
pyinstaller --onefile app.py
```

## Notas
- Asegúrate de activar el entorno virtual antes de instalar dependencias.
- Revisa `Backend/config/settings.py` para configuración adicional.
