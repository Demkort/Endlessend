from flask import Flask, render_template, request, redirect
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Настройка авторизации Google Sheets API через переменную среды
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")

if not credentials_json:
    raise Exception("Переменная окружения GOOGLE_CREDENTIALS_JSON не установлена!")

try:
    creds_dict = json.loads(credentials_json)
except Exception as e:
    raise Exception("Ошибка парсинга GOOGLE_CREDENTIALS_JSON: " + str(e))

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Используй open_by_key — безопаснее, чем по имени
# Замените на свой ID из URL Google Таблицы
SPREADSHEET_ID = "1KEQRkwE0ayBhKFQU6eO_KATtWC-tKS-aRXj3LtdNhpY"  # пример: "1x8AdqR9AiMlYuyr0uEXAMPLEsJ3GSKWnFk12345"

try:
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
except Exception as e:
    raise Exception("Не удалось открыть Google Таблицу. Убедитесь, что ID верный и доступ разрешён.\nОшибка: " + str(e))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    lastname = request.form.get('lastName')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if not name or not lastname or not phone or not email:
        return "Ошибка: все поля обязательны!", 400

    try:
        sheet.append_row([name, lastname, phone, email])
    except Exception as e:
        return f"Ошибка при записи в таблицу: {e}", 500

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
