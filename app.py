import re
from flask import Flask, render_template, request
import json, pandas as pd
import json
from web3 import Web3
from flask import Flask, render_template, url_for
import flask_cors

app = Flask(__name__, static_url_path='/static')
flask_cors.CORS(app)

def web3_get(pt_address):
    # Fill in your infura API key here
    url = "https://d539-2001-44c8-4610-326f-80b7-e289-4217-de24.ap.ngrok.io"
    web3 = Web3(Web3.HTTPProvider(url))
    abi = json.loads("""
	[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "HN",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			}
		],
		"name": "addPatient",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "temp",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "hr",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "spo2",
				"type": "uint256"
			}
		],
		"name": "addVitalSign",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "getPatient",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id",
				"type": "address"
			}
		],
		"name": "getVitalsign",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "ID",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "temp",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "hr",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "spo2",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "time",
						"type": "uint256"
					}
				],
				"internalType": "struct CovidPatients.VitalSign[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
""")

    pt_address = "0x476579e75d2dDd84f2A7b55261558d78aeeb54A2"

    abi_address = "0x68D75e01fcAE9df66056e632f890A4825fBF38F0"
    web3.eth.defaultAccount = web3.eth.accounts[0]
    contract = web3.eth.contract(address=abi_address, abi=abi)
    pt_info = contract.functions.getPatient(pt_address).call()
    ret_data = contract.functions.getVitalsign(pt_address).call()

    str_pt = """
        {
            "name" : "-",
            "HN" : [],
            "address": "-",
            "data" :[]
        }
    """

    json_pt = json.loads(str_pt)
    json_pt['name'] = pt_info[1]
    json_pt['HN'] = pt_info[0]
    json_pt['address'] = pt_address

    for i in ret_data:
        vs = """
        {
                    "timestamp" : 1675503501,
                    "temperature" : 37.0,
                    "heartrate" : 120,
                    "spo2" : 99.0
        }
        """
        json_vs = json.loads(vs)
        json_vs['temperature'] = i[1]
        json_vs['heartrate'] = i[2]
        json_vs['spo2'] = i[3]
        json_vs['timestamp'] = i[4]
        json_pt['data'].append(json_vs)
    return json_pt

@app.route("/")
def home():
    return render_template("home.html")

# @app.route("/css")
# def getCss():
#     return render_template("/static/css/styles.css")

@app.route('/getpt', methods = ['POST'])
#pt_address = request.args.get('address', '')
def getPtByAddr():
    req = request.get_json()
    pt_address = req["walletId"]
    #pt_address = "0xe187c490f39652aDE6CaBdDfc402a52d9d19755E"
    return web3_get(pt_address)


if __name__ == '__main__':
    app.run(debug=True)
