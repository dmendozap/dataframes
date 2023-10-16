from pyexpat.errors import messages

from flask import Flask, request, render_template, redirect
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates')
# app.secret_key = "clave_larga"

# Configura la conexión a PostgreSQL
host = "localhost"
database_name = "ICO_Prices"
user = "postgres"
password = "97B8467b2b*"

# Crea una cadena de conexión SQLAlchemy
connection_string = f"postgresql+psycopg2://{user}:{password}@{host}/{database_name}"

# Crea un motor de SQLAlchemy
engine = create_engine(connection_string)


@app.route("/")
def formulario():
    return render_template("index.html")


@app.route("/importar_excel", methods=["POST"])
def importar_excel():
    mrp_data = request.files['mrpdata']
    df_mrp_data = pd.read_excel(mrp_data)
    df_mrp_data['Material'] = df_mrp_data['Material'].astype(int)
    zptfr = request.files['zptfr']
    df_zptfr = pd.read_excel(zptfr)
    volume = request.files['volume']
    df_volume = pd.read_excel(volume)
    table_name1 = "MRP_DATA"
    table_name2 = "ZPTFR_04"
    table_name3 = "VOLUME_IN"

    df_mrp_data.to_sql(table_name1, con=engine, if_exists='replace', index=False)
    df_zptfr.to_sql(table_name2, con=engine, if_exists='replace', index=False)
    df_volume.to_sql(table_name3, con=engine, if_exists='replace', index=False)

    df_informeconsolidado = df_volume[df_volume['Material'].isin(df_mrp_data['Material'])]
    df_informeconsolidado['Status'] = df_mrp_data['Plant-sp.matl status']
    df_informeconsolidado['Previous Price USD'] = 12.34
    df_informeconsolidado['Actual Price USD'] = 14.06
    df_informeconsolidado['% Variance ICO'] = round(
        df_informeconsolidado['Actual Price USD'] / (df_informeconsolidado['Previous Price USD'] - 1), 2)
    df_informeconsolidado['Variance ICO USD'] = round(
        df_informeconsolidado['Actual Price USD'] - df_informeconsolidado['Previous Price USD'], 2)
    df_informeconsolidado['Comments'] = "NINGUNO"
    columnas_deseadas = ['Material', 'Material Description', 'Profit Center', 'UOM', 'LE2023', 'Status',
                         'Previous Price USD', 'Actual Price USD', '% Variance ICO', 'Variance ICO USD', 'Comments']
    df_informeconsolidado = df_informeconsolidado[columnas_deseadas]
    return render_template('tabla.html', df_informeconsolidado=df_informeconsolidado)

if __name__ == '__main__':
    app.run(debug=True)
