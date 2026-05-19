from fastapi import FastAPI, UploadFile, File, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from db import get_connection
from ai import generate_schema, generate_query
from psycopg2.extras import execute_values

app = FastAPI()

# serve frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("../frontend/index.html")


LAST_TABLE = None


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    global LAST_TABLE

    try:
        df = pd.read_csv(file.file)

        # Fix NaN
        df = df.where(pd.notnull(df), None)

        #  Normalize columns
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        sample = df.head(10).to_dict(orient="records")
        create_query = generate_schema(sample)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(create_query)
        conn.commit()

        table_name = create_query.lower().split("create table")[1].split("(")[0].strip()
        LAST_TABLE = table_name

        insert_query = f"""
        INSERT INTO {table_name} ({','.join(df.columns)})
        VALUES %s
        """

        execute_values(cursor, insert_query, df.values.tolist())

        conn.commit()
        cursor.close()
        conn.close()

        return {
            "message": f"✅ Table '{table_name}' created!",
            "sql": create_query,
            "preview": df.head(5).fillna("").to_dict(orient="records")
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/chat")
async def chat(query: str = Body(...)):
    global LAST_TABLE

    try:
        if not LAST_TABLE:
            return {"error": "Upload CSV first"}

        sql = generate_query(query, LAST_TABLE) # questions into sql conversion

        if "DROP" in sql.upper():
            raise Exception("Unsafe query")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall() if cursor.description else []
        cols = [desc[0] for desc in cursor.description] if cursor.description else []

        cursor.close()
        conn.close()

        results = [dict(zip(cols, row)) for row in rows]

        return {
            "sql": sql,
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}
