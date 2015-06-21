#!/usr/local/bin/python
__author__ = 'randy'
import pythonAir
from flask import Flask, render_template, request,redirect, url_for
import time

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    adapters,monitored = pythonAir.wirelessInterface()
    return render_template('index.html',adapters=adapters, monitored=monitored)
@app.route("/putMonitored", methods=['POST'])
def putMonitored():
    adapter = request.form['adapter']
    pythonAir.PutMonitorMode(adapter)
    time.sleep(5)
    return redirect(url_for('index'))
@app.route('/startScan',methods=['POST'])
def startScan():
    adapter = request.form['mon']
    pythonAir.StartScanningAP(adapter)
    time.sleep(5)
    return redirect(url_for('index'))

@app.route("/stopMonitored", methods=['POST'])
def stopMonitored():
    adapter = request.form['mon']
    pythonAir.stopMonitorMode(adapter)
    time.sleep(5)
    return redirect(url_for('index'))


if __name__=="__main__":
    app.run(host='0.0.0.0',debug = True)
