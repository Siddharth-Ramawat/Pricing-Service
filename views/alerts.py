from flask import Blueprint, request, render_template, redirect, url_for, session
from models.alert import Alert
from models.store import Store
from models.item import Item
from models.user import requires_login


alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/', methods=['GET', 'POST'])
@requires_login
def index():
    alerts = Alert.find_many_by('user_email', session['email'])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_alert():
    """
    For making a new alert we have to follow the following steps
    ~ Get the form data
    ~ Find the store to which the alert is associated to
    ~ Create an Item object
    ~ Find the price of that particular item
    ~ Save the item into the database
    ~ Create an Alert object
    ~ Save the Alert object into the database
    :return: render_template()
    """
    if request.method == 'POST':
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        alert_name = request.form['name']

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)

        item.load_price()
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit, session['email']).save_to_mongo()

    return render_template('alerts/new_alert.html')


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@requires_login
def edit(alert_id):
    alert = Alert.get_by_id(alert_id)
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit

        alert.save_to_mongo()
        return redirect(url_for('.index'))

    return render_template("alerts/edit_alert.html", alert=alert)


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login
def delete(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))
