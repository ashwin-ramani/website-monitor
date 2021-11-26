function create() {
	let formData = new FormData();
	formData.append("purpose", "create");
	["url", "interval"].forEach(item => formData.append(item, document.getElementsByName(item)[0].value));
	fetch("https://website-monitor.ashwinramani1.repl.co/request", {
		"method": "POST",
		"body": formData
	})
	.then(response => response.text())
	.then(data => location.href += data);
}
