from flask import Flask, render_template
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
import os
# from models.item import Item
# from models.alert import Alert

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)

# app.register_blueprint(item_blueprint, url_prefix='/items') # Items are being used internally
app.register_blueprint(alert_blueprint, url_prefix='/alerts')
app.register_blueprint(store_blueprint, url_prefix='/stores')
app.register_blueprint(user_blueprint, url_prefix='/users')


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)


# URL = 'https://www.johnlewis.com/kin-slim-fit-suit-jacket-black/p3399265'
# TAG_NAME = 'span'
# QUERY = {"role": 'text', "class": ''}
# item = Item(URL, TAG_NAME, QUERY)
# item.save_to_mongo()
#
# alert = Alert("5df6228a16764dcf829b1ae66d40f55b", 10000)
# alert.save_to_mongo()
