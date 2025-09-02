from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.testclient import TestClient
from datetime import datetime
import database.oracle_db_config as db
import report_creation

app = FastAPI(
    title="API geração de relatorios Excel",
    version="1.0.0"
)

client = TestClient(app)

def read_sql_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as arquivo:
        return arquivo.read().strip()

def write_log_file(pasta: str, filename: str, content: str) -> None:
    with open(f'log/{pasta}/{filename}_{datetime.now().strftime("%d-%m-%Y")}.log', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"\n{content}")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse('static/favicon.ico', status_code=200)

@app.get("/")
def index():
    return JSONResponse(content={'version': '1.0.0', 'message': 'API geração de relatorios Excel', 'status' : True}, status_code=200)


@app.post('/gerador_relatorio/{file_name}', response_class= JSONResponse)
def rel_produtos(file_name: str, body: dict = Body() ) -> JSONResponse:
    try:
        filtros = body.get('filtros', {})
        extension = body.get('extension', 'xlsx')
        subtitulo = filtros['CODFILIAL'] if 'CODFILIAL' in filtros else 'geral'
        
        sql = read_sql_file(f'sql/{file_name}.sql')

        dados,colunas = db.OracleDBConfig().execute_select(sql, filtros)
        return JSONResponse(
            content= {
                'name': f'{file_name}-{subtitulo}',
                'extension': extension,
                'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'message': 'Relatorio gerado com sucesso', 
                'error' : False,
                'filtros': filtros,
                'colunas': colunas,
                'data' : dados
            },             
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                'name': f'{file_name}-{subtitulo}',
                'extension': extension,                
                'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                'message': f'Erro ao gerar relatorio, erro: {e}', 
                'error' : True,
                'filtros': filtros,                
                'colunas': [],
                'data' : []
            }, 
            status_code=500
        )

async def get_data_report (arquivo: str, body: dict)-> dict:
    response = client.post(f'/gerador_relatorio/{arquivo}', json=body)
    return response.json()
    
@app.post('/criando_excel/{file_name}')
async def criando_excel(file_name: str, body: dict = Body(),) -> JSONResponse:
    try:
        filtros = body.get('filtros', {})
        extension = body.get('extension', 'xlsx')
        subtitulo = filtros['CODFILIAL'] if 'CODFILIAL' in filtros else 'geral'
        
        json = await get_data_report(file_name, body)

        dados = json.get('data', [])
        colunas = json.get('colunas', [])

        report_creation.writeExcel(dados, colunas, f'arquivos-gerados/{file_name}-{subtitulo}', extension)
        
        return JSONResponse(
            content=json, 
            status_code=200
        )
    except Exception as e:
        write_log_file('error', f'{file_name}-{subtitulo}', str(json))
        
        json['message'] = f'Erro ao gerar relatorio, erro: {e}'
        json['error'] = True

        return JSONResponse(
            content= json, 
            status_code=500            
        )