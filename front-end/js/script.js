const error = document.getElementById("error");
const baseUrl = "http://127.0.0.1:5002";

function pushError(errorMsg) {
	console.log(errorMsg);
	error.textContent = errorMsg;
}
function clearError() {
	error.innerText = "";
}

function handelVisibilityPassword(passwordInput, togglePassword) {
	// Toggle the type attribute
	const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
	passwordInput.setAttribute("type", type);

	// Toggle the icon
	togglePassword.classList.toggle("fa-eye");
	togglePassword.classList.toggle("fa-eye-slash");
}

function isLogin() {
	return localStorage.getItem("token") && localStorage.getItem("username");
}

function getURLParameters() {
	var searchParams = new URLSearchParams(window.location.search);
	var params = {};

	// Iterate over all the query parameters
	for (let [key, value] of searchParams) {
		params[key] = value;
	}
	return params;
}

function dropUserFromLocalStorage() {
	localStorage.removeItem("token");
	localStorage.removeItem("username");
}

const logo = document.querySelector(".logoContainer img");
if (logo) {
	logo.addEventListener("click", function () {
		if (location.pathname != "/index.html") {
			location = "/index.html";
		}
	});
}

function autoResize(textarea) {
	textarea.rows = 1;
	let rows = Math.floor((textarea.scrollHeight - 45) / 23) + 1;
	if (rows <= 15) {
		textarea.rows = rows;
	} else {
		textarea.rows = 15;
	}
}
function wait(time) {
	return new Promise((resolve) => setTimeout(resolve, time));
}

function getUsername() {
	return localStorage.getItem("username");
}

function updateURLWithoutReload(url) {
	// Use pushState to update the URL without reloading the page
	history.pushState(null, null, url);
}

async function alertHint(msg, mode = "success") {
	const section = document.querySelector("section.hint ");
	const divAlter = document.querySelector("section.hint > div");
	const alterTitle = document.querySelector("section.hint .alert-title");
	const alterContent = document.querySelector("section.hint .alert-content");

	divAlter.classList.add(`alert-${mode}`);
	alterTitle.innerHTML = mode;
	alterContent.innerText = msg;

	section.classList.add("ActiveAlter");

	await this.wait(100);
	divAlter.id = "ActiveAlter";

	await this.wait(4000);
	divAlter.id = "";
	section.classList.remove("ActiveAlter");
}

function signOut() {
	localStorage.removeItem("username");
	localStorage.removeItem("token");

	window.location = "/login.html";
}
