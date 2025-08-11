from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import  Jinja2Templates
from pydantic import BaseModel
from typing import List
import psycopg2
import psycopg2.extras
from starlette.staticfiles import StaticFiles


def get_db_connection():
        conn = psycopg2.connect(
            host="dpg-d28p0s0gjchc73bueorg-a.oregon-postgres.render.com",
            database="glaim_nails",
            user="sebas",
            password="BSGWtTrUqdgPAQeFyLe56OHEf1DiLQ9B",

        )
        return conn

app = FastAPI()



templates = Jinja2Templates(directory="templates")

app.mount("/staticc", StaticFiles(directory="staticc"), name="staticc")

class Cita(BaseModel):
    nombre: str
    hora_inicio: str
    hora_final: str
    tipo_cita: str
    cita_detallada:str


# Ruta para servir el frontend (HTML)
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/galeria",response_class=HTMLResponse)
async def galeria(request: Request):
    return templates.TemplateResponse("galeria.html", {"request": request})


# API para obtener todas las citas
@app.get("/api/citas", response_model=List[Cita])
def get_citas():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute('SELECT * FROM citass')
    citas = cursor.fetchall()

    cursor.close()
    conn.close()
    result = []
    for cita in citas:
        result.append({
            'nombre': cita['nombre'],
            'hora_inicio': str(cita['hora_inicio']),
            'hora_final': str(cita['hora_final']),
            'tipo_cita': str(cita['tipo_cita']),
            'cita_detallada': str(cita['cita_detallada']),
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
            'INSERT INTO citass (nombre, hora_inicio, hora_final, tipo_cita,cita_detallada) VALUES (%s, %s, %s, %s,%s)',
            (cita.nombre, cita.hora_inicio, cita.hora_final, cita.tipo_cita,cita.cita_detallada)
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
