import dotenv
import os
import oracledb
import base64
import logging as log

class OracleDBConfig:
    
    dbStarted = False

    def __init__(self) -> None:
        try:
            dotenv.load_dotenv()
            self.dbWindowsFile = os.getenv('DB_INITIALIZER_WINDOWS')
            self.dbLinuxFile = os.getenv('DB_INITIALIZER_LINUX')
            
            if(not self.dbWindowsFile or not self.dbLinuxFile):
                raise ValueError('Não foi possível identificar os arquivos do Oracle Client.')
            
            self.start_oracleClient(self.dbWindowsFile, self.dbLinuxFile)
            
            self.dbUser = os.getenv('DB_USERNAME')
            envPassword = os.getenv('DB_PASSWORD')
            
            if envPassword:
                self.dbPassword = base64.b64decode(envPassword).decode('utf-8')  
            else:
                raise ValueError('Não foi possível identificar a senha do banco de dados.')
            
            self.dbHost = os.getenv('DB_HOST')
            self.dbPort = os.getenv('DB_PORT')
            self.dbName = os.getenv('DB_NAME')

            self.dsn = f'{self.dbHost}:{self.dbPort}/{self.dbName}'

            self.connection = oracledb.connect(user=self.dbUser, password=self.dbPassword, dsn=self.dsn)

        except Exception as e:
            log.error(f'Erro ao criar conexão com o banco de dados {self.dbName}, erro: {e}')
    
    @classmethod
    def start_oracleClient(cls, windowsFile: str, linuxFile: str):
        try:
            if cls.dbStarted:
                return
            else:
                if os.name == 'nt':
                    oracledb.init_oracle_client(lib_dir=rf'{windowsFile}')
                else:
                    oracledb.init_oracle_client(lib_dir=rf'{linuxFile}')
                cls.dbStarted = True
        except oracledb.Error as e:
            log.error('Falha na inicialização do cliente Oracle: {e}')

    def execute_select(self, query: str, params: dict = {}):
        try:
            exequery = self.connection.cursor()
            exequery.execute(query, params)
            colunas = [desc[0] for desc in exequery.description]
            dados = exequery.fetchall()
            
            exequery.close()
            # self.connection.close()
            
            return dados, colunas
        except Exception as e:
            log.error(f'Erro ao executar consulta no banco de dados {self.dbName}, erro: {e}')
            raise e
