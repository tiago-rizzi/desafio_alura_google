from flask import Flask, render_template, request
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="chave")

generation_config = {
  "temperature": 0.5,
  }

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "Você é um analista de dados"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/action')
def action():
    return render_template('action.html')

@app.route('/process', methods=['POST'])
def process():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = f"uploads/{uploaded_file.filename}"
        uploaded_file.save(file_path)
        df_ler = pd.read_excel(file_path)
        texto_df = df_ler.to_string()
        
        texto_1 = request.form['texto']
        texto_2 = texto_1 + "\n" + texto_df
        
        convo = model.start_chat(history=[])
        convo.send_message(texto_2)
        resposta = convo.last.text
        resposta_formatada = resposta.replace('**', '<br>').replace('*', '<br>').replace('#', '  ')         
        return render_template('result.html', resposta=resposta_formatada)

if __name__ == '__main__':
    app.run(debug=True)
