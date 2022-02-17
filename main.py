from flask import Flask, render_template, request
import time, requests, threading
from very_important import *

threading.Thread(target = worker, args = (0,), daemon = True).start()
					
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/<monitor_id>")
def _monitor(monitor_id):
	try:
		if (data[monitor_id]["existance-length"] < data[monitor_id]["uptime-length"]):
			data[monitor_id]["existance-length"] = data[monitor_id]["uptime-length"]
		percent = round(data[monitor_id]["uptime-length"] / data[monitor_id]["existance-length"] * 100, 2)
		return f"{data[monitor_id]['readable-status']}<br><br><b>Uptime</b>: {percent}%"
	except ZeroDivisionError:
		if (data[monitor_id]["raw-status"] == "up"):
			percent = 100.0
		else:
			percent = 0.0		
		return f"{data[monitor_id]['readable-status']}<br><br><b>Uptime</b>: {percent}%"
	except KeyError:
		return "Monitor not found."

@app.route("/request", methods = ("POST",))
def handle_request():
	if (request.form["purpose"] == "create"):
		url = request.form["url"].strip()
		monitor_id = generate()
		temp = {
			"url": url,
			"existance-length": 0,
			"uptime-length": 0
		}

	try:
		if (requests.get(url).status_code in {404, 405, 502}):
			raise
		temp["readable-status"] = f"Website <b>{url}</b> is up."
		temp["raw-status"] = "up"
			
	except:
		temp["timestamp"] = time.time()
		temp["raw-status"] = "down"
		temp["readable-status"] = f"Website <b>{url}</b> is down - recorded as down 0 seconds ago."

	atw(monitor_id)

	data[monitor_id] = temp
	return monitor_id
			
app.run("0.0.0.0")
