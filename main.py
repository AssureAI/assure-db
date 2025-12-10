from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import psycopg2

app = FastAPI()
templates = Jinja2Templates(directory=".")

DATABASE_URL = os.environ["DATABASE_URL"]

def run_sql(sql: str):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("sql_form.html", {"request": request})

@app.post("/run")
def run(request: Request, sql: str = Form(...)):
    try:
        run_sql(sql)
        result = "Success"
    except Exception as e:
        result = f"Error: {e}"
    return templates.TemplateResponse("sql_form.html", {"request": request, "result": result})
