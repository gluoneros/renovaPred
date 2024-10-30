from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

with open('modelo.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        
        # Convertir strings a floats antes de la predicción
        try:
            latitud = float(latitud)
            longitud = float(longitud)
        except ValueError:
            return render_template('index.html', prediction="Error: Ingrese valores numéricos para latitud y longitud")

        cordenadas = [latitud, longitud]  
        prediction = model.predict([cordenadas])
        print(prediction)
        
        # Interpretar la predicción y generar el mensaje
        if prediction == 1:
            viavilidad = "Apto para proyecto solar"
        elif prediction == 2:
            viavilidad = "Apto para proyecto eólico"
        elif prediction == 3:
            viavilidad = "Apto para proyecto eolico y solar"
        else:
            viavilidad = "No apto para proyecto solar o eólico"
        
        return render_template('index.html', prediction=f'El resultado es: {viavilidad}')
if __name__ == '__main__':
    app.run(debug=True, port=5001)