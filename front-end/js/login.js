if (isLogin()) {
	window.location = "/dashboard.html";
}

window.addEventListener("load", function () {
	const urlParams = getURLParameters();

	// Check if the email and password are in the URL parameters
	if (urlParams.hasOwnProperty("email") && urlParams.hasOwnProperty("password")) {
		email.value = urlParams.email;
		password.value = urlParams.password;
		updateURLWithoutReload(location.pathname);
	}
});

const loginForm = document.querySelector("form");
const email = document.querySelector('input[type="email"]');
const password = document.querySelector('input[type="password"]');

loginForm.addEventListener("submit", async function (event) {
	event.preventDefault();

	const emailValue = email.value;
	const passwordValue = password.value;

	const data = {
		email: emailValue,
		password: passwordValue,
	};

	try {
		const response = await fetch(`${baseUrl}/login`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		if (!response.ok) {
			const errorData = await response.json();
         
			alertHint(errorData.error, "warning");
			return;
		}

		const responseData = await response.json();
		localStorage.setItem("token", responseData.token);
		localStorage.setItem("username", responseData.username);

		window.location.href = "/dashboard.html";
	} catch (error) {
		console.log(error)
		alertHint("error ", "danger");
	}
});

const togglePassword = document.getElementById("togglePassword");
togglePassword.addEventListener("click", function () {
	handelVisibilityPassword(password, this);
});
