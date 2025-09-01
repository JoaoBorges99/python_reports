import fastapi
from fastapi.responses import JSONResponse

app = fastapi.FastAPI(
    title="API geração de relatorios Excel",
    version="1.0.0"
)

@app.get("/")
def index():
    return JSONResponse(content={'version': '1.0.0', 'message': 'API geração de relatorios Excel', 'status' : True}, status_code=200)