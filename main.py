from flask import Flask, render_template, request, redirect
import threading, time, requests, random, json

app = Flask("__main__")

with open("data.json") as file:
	data = json.loads(file.read())

def generate():
	def generate_str():
		chars = []
		for i in range(15):
			char_type = random.choice(("int", "str"))
			if (char_type == "int"):
				 chars.append(str(random.randint(0, 9)))
			else:
				chars.append(random.choice("abcdefghijklmnopqrstuvwxyz"))
			
		return "".join(chars)
	
	generated = generate_str()
	while generated in data["monitors"]:
		generated = generate_str()
	return generated

def uptime(monitor, interval):
	if (interval < 1): 
		interval = 1
	while True:
		try:
			status = requests.get(data["monitors"][monitor]["url"]).status_code
			if (not(status in (429, 444) or str(status).startswith("2"))): 
				raise "error"
			data["monitors"][monitor]["status"] = f"Website {data['monitors'][monitor]['url']} is up."
		except:
			data["monitors"][monitor]["status"] = f"Website {data['monitors'][monitor]['url']} is down."

		data["monitors"][monitor]["sent"] += 1
		
		time.sleep(interval)

@app.route("/") 
def index():
	return render_template("index.html")

@app.route("/<monitor>")
def load(monitor):
	if (not(monitor in data["monitors"])):
		return redirect("/")
	else:
		return f"<title>Monitor</title><b>{data['monitors'][monitor]['status']}</b><br>Sent: {data['monitors'][monitor]['sent']}"

@app.route('/request', methods = ["POST"])
def respond():
	if (request.form["purpose"] == "create"):

		monitorID = generate()
		status = None
		try:
			status = requests.get(request.form["url"]).status_code
			if (not(status in (405, 429, 444) or str(status).startswith("2"))):
				 raise "error"
			status = f"Website {request.form['url']} is up."
		except:
			status = f"Website {request.form['url']} is down."

		data["monitors"][monitorID] = {"status": status, "url": request.form["url"], "monitor": monitorID, "sent": 0}
		
		t = None

		try:
			t = threading.Thread(target = uptime, args = (monitorID, int(request.form["interval"])))
		except:
			t = threading.Thread(target = uptime, args = (monitorID, 1))
		
		t.start()

		return monitorID


app.run(host = "0.0.0.0")
