from flask import Flask, render_template, url_for, request, redirect
from time import gmtime, strftime

app = Flask(__name__)

patients = [
    {
    'id': 1,
    'uuid': 'xxx',
    'name': 'Patient',
    'surname': 'First',
    'pesel': '93021548556',
    'date_admission': '2017-02-18',
    'info': 'Double Cancer',
    'date_modified': '2017-02-18 12:00'
    },
    {
    'id': 2,
    'uuid': 'xxx',
    'name': 'Patient',
    'surname': 'Third',
    'pesel': '93021548556',
    'date_admission': '2018-02-08',
    'info': 'Cancer',
    'date_modified': '2017-05-02 12:00'
    }
]

@app.route("/")
def list():
    return render_template('list.html', patients=patients)

@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/add", methods=['GET'])
def add_form():
    return render_template('add.html', title='add patient')

@app.route("/add", methods=['POST'])
def add():
    form = request.form
    patient = {}
    mapPatient(patient, form, patients[-1]['id'] + 1)
    patients.append(patient)
    return redirect("/")

@app.route("/edit", methods=['GET'])
def edit_form():
    id = request.args.get('id', default = 1, type = int)
    form = patients[id-1]
    return render_template('edit.html', title='edit patient', form=form)

@app.route("/edit", methods=['POST'])
def edit():
    form = request.form
    for index, item in enumerate(patients):
        if item['id'] == int(form['id']):
            mapPatient(item, form, item['id'])
    return redirect("/")

def mapPatient(patient, form, id):
    patient['id'] = id
    patient['uuid'] = 'xxx'
    patient['name'] = form['firstname']
    patient['surname'] = form['surname']
    patient['pesel'] = form['pesel']
    patient['date_admission'] = form['date_admission']
    patient['info'] = form['info']
    patient['date_modified'] = strftime("%Y-%m-%d %H:%M", gmtime())

app.run(debug=True, host='127.0.0.1', port=5000)
