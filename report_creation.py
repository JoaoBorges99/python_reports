import pandas as pd

def writeExcel(data: list, colunas: list, file_name:str, extension: str = 'xlsx'):
    df = pd.DataFrame(data, columns=colunas)
    if extension == 'xlsx':
        df.to_excel(f'{file_name}.{extension}', index=False)
    elif extension == 'csv':
        df.to_csv(f'{file_name}.{extension}', index=False)
    else:
        raise ValueError('Extensão não suportada, use xlsx ou csv')
    