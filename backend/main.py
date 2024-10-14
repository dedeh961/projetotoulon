from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error
import os

app = FastAPI()

# Configuração do MinIO
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://localhost:9000')

client = Minio(
    MINIO_ENDPOINT.replace('http://', ''),
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

bucket_name = "csv-bucket"

origins = [
    "http://localhost:8080",  # Vue.js
    "http://localhost:8000"
]

# comunicacao entre backend e frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

found = client.bucket_exists(bucket_name)

if not found:
    client.make_bucket(bucket_name)

@app.get("/ListaDeCSVs")
async def lista_de_csvs():
    try:
        objetos_do_minio = client.list_objects(bucket_name)

        url_base = "http://localhost:8000/BaixarCSV/"

        lista_de_arquivos = [{"nome": obj.object_name, "url": url_base + obj.object_name} for obj in objetos_do_minio if obj.object_name.endswith('.csv')]

        return {"lista_de_arquivos": lista_de_arquivos}

    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/EnviarCSV/")
async def enviar_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Apenas arquivos CSV são permitidos")
    
    try:
        client.put_object(bucket_name, file.filename, file.file, length=-1, part_size=10*1024*1024)

        return {"message": "Arquivo enviado com sucesso"}

    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/BaixarCSV/{nome_do_arquivo}")
async def baixar_csv(nome_do_arquivo: str):
    try:
        objeto_do_minio = client.get_object(bucket_name, nome_do_arquivo)

        conteudo_do_csv = objeto_do_minio.read()

        objeto_do_minio.close()

        objeto_do_minio.release_conn()

        return Response(
            content=conteudo_do_csv,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={nome_do_arquivo}"}
        )

    except S3Error as e:
        return Response(content=str(e), status_code=500)
