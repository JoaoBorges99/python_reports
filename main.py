from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.testclient import TestClient
import database.oracle_db_config as db
from datetime import datetime

app = FastAPI(
    title="API geração de relatorios Excel",
    version="1.0.0"
)

client = TestClient(app)

def read_sql_file(filename: str) -> str:
    with open(filename, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def write_log_file(pasta: str, filename: str, content: str) -> None:
    with open(f'log/{pasta}/{filename}_{datetime.now().strftime("%d-%m-%Y")}.log', 'a', encoding='utf-8') as arquivo:
        arquivo.write(f"\n{content}")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse('static/favicon.ico', status_code=200)

@app.get("/")
def index():
    return JSONResponse(content={'version': '1.0.0', 'message': 'API geração de relatorios Excel', 'status' : True}, status_code=200)


@app.get('/gerador_relatorio/{file_name}', response_class= JSONResponse)
def rel_produtos(file_name: str) -> JSONResponse:
    try:
        sql = read_sql_file(f'sql/{file_name}.sql')
        dados = db.OracleDBConfig().execute_select(query=sql)
        return JSONResponse(
            content={
                'name': file_name, 
                'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                'message': 'Relatorio gerado com sucesso', 
                'error' : False, 
                'data' : dados
            }, 
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                'name': file_name, 
                'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
                'message': f'Erro ao gerar relatorio, erro: {e}', 
                'error' : True, 
                'data' : []
            }, 
            status_code=500
        )

async def get_data_report (arquivo: str) -> dict:
    response = client.get(f'/gerador_relatorio/{arquivo}')
    return response.json()['data']
    
@app.get('/criando_excel/{file_name}/{filial}')
async def criando_excel(file_name: str, filial: str,):
    try:
        dados = await get_data_report(file_name+'kds')

        if not dados:
            raise ValueError('Nenhum dado encontrado para gerar o relatorio')
        
        return JSONResponse(
            content= {
                'name': file_name+filial,
                'extension': '',
                'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'message': 'Relatorio excel escrito com sucesso', 
                'error' : False, 
                'data' : dados
            }, 
            status_code=200
        )
    except Exception as e:
        conteudo = {
            'name': file_name+filial,
            'extension': '',
            'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 
            'message': f'Erro ao escrever relatorio, erro: {e}', 
            'error' : True, 
            'data' : []
        }

        write_log_file('error', f'{file_name}_{filial}', str(conteudo))

        return JSONResponse(
            content= conteudo, 
            status_code=500            
        )