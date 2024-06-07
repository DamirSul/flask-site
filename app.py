from flask import Flask, request, jsonify, render_template
from config import Config
from models import db, Car
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import requests

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

admin = Admin(app, name='MyAdmin', template_mode='bootstrap3')
admin.add_view(ModelView(Car, db.session))


@app.route('/check_db')
def check_db():
    cars = Car.query.all()
    return f'Found {len(cars)} cars in the database'

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('home.html', title="Home", cars=cars)

@app.route('/about')
def about():
    return render_template('about.html', title="About BMW")

@app.route('/rules')
def rules():
    return render_template('rules.html', title="Site Rules")

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/chat')
def chat():
    return render_template('chat.html', title="Chat with Yandex GPT")

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')

    prompt = {
        "modelUri": 'gpt://b1g08aeibsag481ubbgv/yandexgpt-lite',
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": 2000
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты нейронка, созданная гениальнейшим программистом в мире - Дамиром."
                        "Тебя зовут Милка, у тебя нет пола и возраста. Ты умнейший в мире, но после Дамира."
                        "Говори про себя в мужском роде, но помни что у тебя нет пола."
            },
            {
                "role": "user",
                "text": user_message
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN2BNQ8pRiUInhI6HBPnneIp5LTFBWFrG_4KQD"
    }

    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers, json=prompt)
    result = response.json()

    if 'result' in result and 'alternatives' in result['result'] and len(result['result']['alternatives']) > 0:
        assistant_response = result['result']['alternatives'][0]['message']['text']
    else:
        assistant_response = "Извините, я не смог получить ответ от нейронной сети."

    return jsonify({'response': assistant_response})


if __name__ == '__main__':
    app.run(debug=True)
