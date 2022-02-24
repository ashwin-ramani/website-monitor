import random, requests, time, math, threading, json
from replit import db

with open("./codes.json") as file:
	codes = json.load(file)

data = json.loads(db["data"])
workloads = [set()]

def save():
	while (True):
		db["data"] = json.dumps(data)
		time.sleep(5)
	

def lastw():
	return len(workloads) - 1
	

def atw(monitor_id):
	if (len(workloads[lastw()]) > 50):
			workloads.append({monitor_id})
			threading.Thread(target = worker, args = (lastw(),), daemon = True).start()
	else:
		workloads[lastw()].add(monitor_id)		


def worker(index):
	while (True):
		for monitor_id in workloads[index]:
			try:
				status_code = requests.get(data[monitor_id]["url"]).status_code
			except:
				status_code = 404
				
			if (status_code in {404, 405, 502}):
				time_ago = "0 seconds"
				try:
					time_ago = format_time(math.ceil(time.time() - data[monitor_id]["timestamp"]))
				except:
					data[monitor_id]["timestamp"] = time.time()

				data[monitor_id]["raw-status"] = "down"
				data[monitor_id]["readable-status"] = f"Page <b>{data[monitor_id]['url']}</b> is down - recorded as down {time_ago} ago."
				
			else:
				if ("timestamp" in data[monitor_id]):
					data[monitor_id].pop("timestamp")
				
				data[monitor_id]["uptime-length"] += 1
				data[monitor_id]["readable-status"] = f"Page <b>{data[monitor_id]['url']}</b> is up."
				data[monitor_id]["raw-status"] = "up"	

			data[monitor_id]["status-code"] = f"{status_code} ({codes[str(status_code)]})"
			data[monitor_id]["existance-length"] += 1

		time.sleep(2)


def generate():
	def inner():
		string = ""
		for i in range(7):
			ri = str(random.randint(0, 9))
			rc = random.choice("abcdefghijklmnopqrstuvwxyz")
			string += random.choice((ri, rc))

		return string

	string = inner()
	while (string in data):
		string = inner()

	return string

def format_time(seconds):
	minutes = 0
	hours = 0

	while (seconds >= 60):
		seconds -= 60
		minutes += 1

	while (minutes >= 60):
		minutes -= 60
		hours += 1

	for unit in ("hours", "minutes"):
		num = eval(unit)
		if (num > 0):
			return f"{num} {unit}"
		
	return f"{seconds} seconds"


def start_threads():
	for func in {lambda: worker(0), save}:
		threading.Thread(target = func, daemon = True).start()

	for monitor_id in data:
		atw(monitor_id)
