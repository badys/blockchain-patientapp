from flask import Flask, render_template, url_for, request, redirect
from time import gmtime, strftime
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

app = Flask(__name__)


def connect_to_blockchain():
    # web3 instance
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    docmed = w3.eth.contract(address=ADDRESS, abi=ABI)
    return w3, docmed


def read_all_patients():
    patients = []
    for i in range(docmed.functions.getPatientsNo().call()):
        patients.append(jsonifyPatient(docmed.functions.patients(docmed.functions.patientIds(i).call()).call()))
    return patients


def jsonifyPatient(patient):
    return {"wallet": patient[0], "pesel": patient[1], "firstname": patient[2], "lastname": patient[3],
            "resNo": patient[4], "inHospital": patient[5], "residances": {}}


def read_all_doctors():
    doctors = []
    for i in range(docmed.functions.getDoctorsNo().call()):
        doctors.append(jsonifyDoctor(docmed.functions.doctors(docmed.functions.doctorIds(i).call()).call()))
    return doctors


def jsonifyDoctor(doctor):
    return {"wallet": doctor[0], "doctorNPWZ": doctor[1], "firstname": doctor[2], "lastname": doctor[3]}


@app.route("/")
def list():
    return render_template('list.html', patients=read_all_patients(), doctors=read_all_doctors())


@app.route("/about")
def about():
    return render_template('about.html', title='about')


@app.route("/patient/add", methods=['GET'])
def patient_add_form():
    return render_template('addPatient.html', title='add patient')


@app.route("/patient/add", methods=['POST'])
def patient_add():
    form = request.form
    w3.eth.waitForTransactionReceipt(docmed.functions.registerPatient(form['pesel'], form['firstname'], form['surname']).transact())
    return redirect("/")


@app.route("/doctor/add", methods=['GET'])
def doctor_add_form():
    return render_template('addDoctor.html', title='add patient')


@app.route("/doctor/add", methods=['POST'])
def doctor_add():
    form = request.form
    w3.eth.waitForTransactionReceipt(docmed.functions.registerDoctor(w3.eth.accounts[0], int(form['npwz']), form['firstname'], form['surname']).transact())
    return redirect("/")


with open("data.json", 'r') as f:
    data = json.load(f)
    ABI = data["abi"]
    ADDRESS = data["address"]

#Connecting to blockchain
w3, docmed = connect_to_blockchain()

app.run(debug=True, host='127.0.0.1', port=5000)
