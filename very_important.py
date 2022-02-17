import random, requests, time, math, threading

data = {}
workloads = [set()]


def lastw():
	return len(workloads) - 1
	

def atw(monitor_id):
	if (len(workloads[lastw()]) > 50):
			workloads.append({monitor_id})
			threading.Thread(target = worker, args = (lastw(),), daemon = True).start()
	else:
		workloads[lastw()].add(monitor_id)		


def worker(i):
	while (True):
		for monitor_id in workloads[i]:
			try:
				if (requests.get(data[monitor_id]["url"]).status_code in (404, 405, 502)):
					raise
					
				else:
					if ("timestamp" in data[monitor_id]):
						data[monitor_id].pop("timestamp")
					
					data[monitor_id]["uptime-length"] += 1
					data[monitor_id]["readable-status"] = f"Website <b>{data[monitor_id]['url']}</b> is up."
			except:
				seconds = 0
				if ("timestamp" in data[monitor_id]):
					seconds = math.ceil(time.time() - data[monitor_id]["timestamp"])
				else:
					data[monitor_id]["timestamp"] = time.time()

				data[monitor_id]["readable-status"] = f"Website <b>{data[monitor_id]['url']}</b> is down - recorded as down {seconds} seconds ago."	

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
