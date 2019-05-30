from flask import Flask, render_template, url_for, request, redirect, jsonify
from time import gmtime, strftime
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import datetime

app = Flask(__name__)


def connect_to_blockchain():
    # web3 instance
    print('Connecting...')
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3.middleware_stack.inject(geth_poa_middleware, layer=0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    docmed = w3.eth.contract(address=ADDRESS, abi=ABI)
    print('Connected !' if w3.isConnected() else 'Error while connecting!')
    return w3, docmed


def refillAccounts():
    print('Refilling ethereum in accounts')
    for i in w3.personal.listAccounts:
        w3.eth.sendTransaction({'from': w3.eth.coinbase, 'to': i, 'value': 1000000000000000000000})
    print('Refilling finished')


def read_all_patients():
    patients = []
    for i in range(patCount()):
        patient = docmed.functions.patients(docmed.functions.patientIds(i).call()).call()
        residents = []
        for resNo in range(patient[4]):
            visitNo = docmed.functions.getPatientResidanceVisitsNo(patient[0], resNo).call()
            visits = []
            for visit in range(visitNo):
                docWallet, timemili, recom = docmed.functions.getPatientResidanceVisitInfo(patient[0], resNo, visit).call()
                timestamp = datetime.datetime.fromtimestamp(timemili)
                doc = jsonifyDoctor(docmed.functions.doctors(docWallet).call())
                visits.append({'visitNo': visit + 1, 'recommendation': recom, 'date': timestamp.strftime("%Y-%m-%d %H:%M"), 'doc': doc['firstname'] + " " + doc['lastname']})

            residents.append({'resNo': resNo + 1, 'visits': visits})
        patients.append(jsonifyPatient(patient, residents))
    return patients


def jsonifyPatient(patient, residents):
    return {"wallet": patient[0], "pesel": patient[1], "firstname": patient[2], "lastname": patient[3],
            "resNo": patient[4], "inHospital": patient[5], "residances": residents}


def read_all_doctors():
    doctors = []
    for i in range(docCount()):
        doctors.append(jsonifyDoctor(docmed.functions.doctors(docmed.functions.doctorIds(i).call()).call()))
    return doctors


def jsonifyDoctor(doctor):
    return {"wallet": doctor[0], "doctorNPWZ": doctor[1], "firstname": doctor[2], "lastname": doctor[3]}


def docCount():
    return docmed.functions.getDoctorsNo().call()


def patCount():
    return docmed.functions.getPatientsNo().call()


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
    w3.eth.waitForTransactionReceipt(
        docmed.functions.registerPatient(form['pesel'], form['firstname'], form['surname']).transact({'from': PATIENTS_ADDRESS[patCount()], 'gas': 1000000}))
    return redirect("/")

@app.route("/patient/addVisit", methods=['POST'])
def patient_add_visit():
    form = request.form
    w3.eth.waitForTransactionReceipt(
        docmed.functions.addVisit(form['patientWallet'], form['recommendations']).transact({'from': form['doctor'], 'gas': 1000000}))
    return redirect("/")

@app.route("/patient/endVisit", methods=['POST'])
def patient_end_visit():
    form = request.form
    w3.eth.waitForTransactionReceipt(
        docmed.functions.endResidance(form['patientWallet']).transact({'from': form['doctor'], 'gas': 1000000}))
    return redirect("/")


@app.route("/doctor/add", methods=['GET'])
def doctor_add_form():
    return render_template('addDoctor.html', title='add patient')


@app.route("/doctor/add", methods=['POST'])
def doctor_add():
    form = request.form
    w3.eth.waitForTransactionReceipt(
        docmed.functions.registerDoctor(DOCTORS_ADDRESS[docCount()], int(form['npwz']), form['firstname'], form['surname']).transact({'from': w3.eth.accounts[0], 'gas': 1000000}))
    return redirect("/")


@app.route("/refill", methods=['GET'])
def refill():
    try:
        refillAccounts()
        message="All good"
    except:
        message="Error while refilling"
    return jsonify(message=message)


with open("data.json", 'r') as f:
    data = json.load(f)
    ABI = data["abi"]
    ADDRESS = data["address"]
    PATIENTS_ADDRESS = data["patients"]
    DOCTORS_ADDRESS = data["doctors"]

# Connecting to blockchain
w3, docmed = connect_to_blockchain()
refillAccounts()

app.run(debug=True, host='127.0.0.1', port=5000)
