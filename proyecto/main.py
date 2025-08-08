from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import  Jinja2Templates
from pydantic import BaseModel
from typing import List
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('identifier.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Cambia según el puerto que uses para frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="proyecto/templates")

# Modelo Pydantic para validación del POST
class Cita(BaseModel):
    nombre: str
    hora_inicio: str
    hora_final: str
    estado: str


# Ruta para servir el frontend (HTML)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# API para obtener todas las citas
@app.get("/api/citas", response_model=List[Cita])
async def get_citas():
    conn = get_db_connection()
    citas = conn.execute('SELECT * FROM citass').fetchall()
    result = []
    for cita in citas:
        result.append({
            'nombre': cita['nombre'],
            'hora_inicio': str(cita['hora_inicio']),
            'hora_final': str(cita['hora_final']),
            'estado': cita['estado'],
        })
    return result


# API para agregar nueva cita
@app.post("/api/citas", status_code=201)
async def add_cita(cita: Cita):
    if cita.hora_final <= cita.hora_inicio:
        raise HTTPException(status_code=400, detail="La hora final debe ser posterior a la hora de inicio")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO citass (nombre, hora_inicio, hora_final, estado) VALUES (?, ?, ?, ?)',
            (cita.nombre, cita.hora_inicio, cita.hora_final, cita.estado)
        )
        conn.commit()
        return {"message": "Cita agregada correctamente", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
