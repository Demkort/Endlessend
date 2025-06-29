from flask import Flask, render_template, request, redirect
import gspread
import os, json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Авторизация в Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
creds_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Открываем таблицу по названию
sheet = client.open("Endlessend").sheet1  # Имя таблицы в Google Sheets

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    lastname = request.form.get('lastName')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if not name or not lastname or not phone or not email:
        return "Ошибка: не все поля заполнены", 400

    # Добавляем строку в таблицу
    sheet.append_row([name, lastname, phone, email])

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
