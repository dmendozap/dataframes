from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__, template_folder='templates')
app.secret_key = "clave_larga"


@app.route("/")
def formulario():
    return render_template("index.html")


@app.route("/importar_excel", methods=["POST"])
def importar_excel():
    lista = []
    archivo = request.files['archivosq']
    df = pd.read_excel(archivo)
    df['ValorTotal'] = df['PrecioUnidad'] * df['UnidadesEnExistencia']
    df['PrecioVenta'] = (df['ValorTotal'] * 0.10 / 100) + df['ValorTotal']
    df_resultado = (
        df.loc[:, ['NombreProducto', 'Proveedor', 'PrecioUnidad', 'UnidadesEnExistencia', 'ValorTotal', 'PrecioVenta']])

    return render_template('tabla.html', tabla=[df_resultado.to_html(classes='data')], titles=df.columns.values)


if __name__ == '__main__':
    app.run()
