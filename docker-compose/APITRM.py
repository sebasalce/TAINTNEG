import requests
import pandas as pd
from saveS3 import SaveS3

limit =20
ENDPOINT_API = f'https://www.datos.gov.co/resource/32sa-8pi3.json?$limit={limit}'

def getData():
    req = requests.get(ENDPOINT_API)
    if req.status_code == 200:
        dat = req.json()
        return dat
    else:
        print("Error al obtener los datos:", req.status_code)
        return None

def create_empty_dataframe():
    # Definir un DataFrame vacío con columnas específicas y tipos de datos
    df = pd.DataFrame({
        'valor': pd.Series(dtype='float'),
        'unidad': pd.Series(dtype='object'),
        'vigenciadesde': pd.Series(dtype='datetime64[ns]'),
        'vigenciahasta': pd.Series(dtype='datetime64[ns]')
    })
    return df

def fill_dataframe(df, data):
    # Crear un DataFrame temporal con los datos y concatenarlo al DataFrame vacío
    temp_df = pd.DataFrame(data)
    print("Tipos de datos del DataFrame temporal antes de la conversión:")
    print(temp_df.dtypes)
    
    temp_df['valor'] = temp_df['valor'].astype(float)
    temp_df['unidad'] = temp_df['unidad'].astype(str)
    temp_df['vigenciadesde'] = pd.to_datetime(temp_df['vigenciadesde']).dt.date
    temp_df['vigenciahasta'] = pd.to_datetime(temp_df['vigenciahasta']).dt.date
    
    print("Tipos de datos del DataFrame temporal después de la conversión:")
    print(temp_df.dtypes)
    
    df = pd.concat([df, temp_df], ignore_index=True)
    return df

def transformaciones(df):
    df['vigenciadesde'] = pd.to_datetime(df['vigenciadesde'])
    df['vigenciahasta'] = pd.to_datetime(df['vigenciahasta'])
        # Agregar columnas de día, mes y año
    # df['dia'] = df['vigenciadesde'].dt.day
    # df['mes'] = df['vigenciadesde'].dt.month
    # df['anio'] = df['vigenciadesde'].dt.year
    return df

# Obtener los datos de la API
dat = getData()

# Crear el DataFrame vacío
df = create_empty_dataframe()
print(df.head())
# Llenar el DataFrame con los datos
df = fill_dataframe(df, dat)
print(df.head())
# Aplicar las transformaciones
df = transformaciones(df)
print(df.head())

#Guardar en S3 (descomentar estas líneas cuando tengas la función SaveS3 implementada)
up1 = SaveS3(df, 'trmbucket', 'TRMCOP')
s3_obj1 = up1.write_to_minio_parquet()
print(s3_obj1)
