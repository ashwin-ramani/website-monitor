from flask import Flask, render_template, request
import time, requests, threading, re
from stuff import *

start_threads()

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")\
	

@app.route("/<monitor_id>")
def _monitor(monitor_id):
	try:
		if (data[monitor_id]["existance-length"] < data[monitor_id]["uptime-length"]):
			data[monitor_id]["existance-length"] = data[monitor_id]["uptime-length"]
		percent = round(data[monitor_id]["uptime-length"] / data[monitor_id]["existance-length"] * 100, 2)
	except ZeroDivisionError:
		if (data[monitor_id]["raw-status"] == "up"):
			percent = 100.0
		else:
			percent = 0.0		
	except KeyError:
		return "Monitor not found."

	return f"{data[monitor_id]['readable-status']}<br><br><b>Status Code</b>: {data[monitor_id]['status-code']}<br><br><b>Uptime</b>: {percent}%"

@app.route("/request", methods = {"POST"})
def handle_request():
	if (request.form["purpose"] == "create"):
		url = request.form["url"].strip()
		if (re.match("^(https?://)", url) == None):
			url = f"http://{url}"
		monitor_id = generate()
		try:
			status_code = requests.get(url).status_code
		except:
			return f"URL \"{url}\" does not exist."
		temp = {
			"url": url,
			"status-code": f"{status_code} ({codes[str(status_code)]})",
			"existance-length": 0,
			"uptime-length": 0
		}

	try:
		if (status_code in {404, 405, 502}):
			raise
		temp["readable-status"] = f"Page <b>{url}</b> is up."
		temp["raw-status"] = "up"
		
	except:
		temp["timestamp"] = time.time()
		temp["raw-status"] = "down"
		temp["readable-status"] = f"Page <b>{url}</b> is down - recorded as down 0 seconds ago."

	atw(monitor_id)

	data[monitor_id] = temp
	return monitor_id

app.run("0.0.0.0")
