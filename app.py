from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)

customers = [
    {
        'id': 1,
        'firstName': 'Stacey',
        'lastName': 'Smith',
        'isPremiumMember': False
    },
    {
        'id': 2,
        'firstName': 'Jack',
        'lastName': 'Jackson',
        'isPremiumMember': True
    }
]

@app.route('/api/1.0/customers', methods=['GET'])
def getCustomers():
    return jsonify({'customers': customers})

@app.route('/api/1.0/customers/<int:customerId>', methods=['GET'])
def geCustomer(customerId):
    customer = [customer for customer in customers if customer['id'] == customerId]
    if len(customer) == 0:
        return render_template("notFound.html")
        #abort(404)
    return jsonify({'customer': customer[0]})
    
@app.route('/api/1.0/customers', methods=['POST'])
def createCustomer():
    if not request.json:
        abort(400)
    customer = {
        'id': customers[-1]['id'] + 1,
        'firstName': request.json.get('firstName'),
        'lastName': request.json.get('lastName'),
        'isPremiumMember': request.json.get('isPremiumMember')
    }
    customers.append(customer)
    return jsonify({'customer': customer}), 201

@app.route('/api/1.0/customers/<int:customerId>', methods=['DELETE'])
def deleteCustomer(customerId):
    customer = [customer for customer in customers if customer['id'] == customerId]
    if len(customer) == 0:
        abort(404)
    customers.remove(customer[0])
    return jsonify({'result': True})

@app.route('/api/1.0/customers/<int:customerId>', methods=['PUT'])
def updateCustomer(customerId):
    customer = [customer for customer in customers if customer['id'] == customerId]
    if len(customer) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'firstName' in request.json and type(request.json['firstName']) != unicode:
        abort(400)
    if 'lastName' in request.json and type(request.json['lastName']) is not unicode:
        abort(400)
    if 'isPremiumMember' in request.json and type(request.json['isPremiumMember']) is not bool:
        abort(400)
    customer[0]['firstName'] = request.json.get('firstName', customer[0]['firstName'])
    customer[0]['lastName'] = request.json.get('lastName', customer[0]['lastName'])
    customer[0]['isPremiumMember'] = request.json.get('isPremiumMember', customer[0]['isPremiumMember'])
    return jsonify({'customer': customer[0]})

@app.route("/")
def home():
    return render_template("index.html")