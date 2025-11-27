from flask import Flask, request
import pandas as pd
import pickle
from sqlalchemy import create_engine

app = Flask(__name__)

with open("model.pkl", "rb") as archivo:
    modelo = pickle.load(archivo) # load para leer el archivo

churro = 'postgresql://mypostgres_njxk_user:66fLtLNl757NYqK3rlPTTU2svjffZjmL@dpg-d4k3b563jp1c738ieiag-a.ohio-postgres.render.com/mypostgres_njxk'
engine = create_engine(churro)

@app.route("/", methods=["GET"])
def hola():
    return "Todo ok"

@app.route("/predict", methods=["GET"])
def predict():
    age = request.args.get("age", None)
    sex = request.args.get("sex", None)
    clase = request.args.get("clase", None)

    if age is None or sex is None or clase is None:
        return "No se ha encontrado los parametros"
    
    if not (str(age).isnumeric() or str(sex).isnumeric() or str(clase).isnumeric()):
        return """<h1>Tiene que ser un número <h1 style="color:red">¡melón!<h1>"""
    
    age = int(age)
    sex = int(sex)
    clase = int(clase)

    survived = "Sobrevivio" if modelo.predict([[age, sex, clase]])[0] else "Palmo"

    df = pd.DataFrame({"sex": [sex], "age":[age], "class": [clase], "prediction":[survived]})
    df.to_sql("predictions", con=engine, if_exists="append", index=None)

    return f"""Para la persona con {age} años, sexo {sex} y clase {clase}, la prediccion es {survived}"""

if __name__ == "__main__":
    app.run(debug=True)