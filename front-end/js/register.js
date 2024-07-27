if(isLogin()){
	window.location = "/dashboard.html";
}
const registerForm = document.querySelector("form");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirmPassword");






registerForm.addEventListener("submit", async function (event) {
	event.preventDefault();

	const usernameValue = username.value;
	const emailValue = email.value;
	const passwordValue = password.value;
	const confirmPasswordValue = confirmPassword.value;

	if (passwordValue !== confirmPasswordValue) {
		console.log("nice");
		pushError("Passwords do not match");
		return;
	}

	const data = {
		username: usernameValue,
		email: emailValue,
		password: passwordValue,
	};

	try {
		const response = await fetch(`${baseUrl}/register`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		});

		if (!response.ok) {
			const errorData = await response.json();
			console.log(errorData);
			alertHint(errorData.message, "warning");
			return;
		}

		const responseData = await response.json();

		window.location.href = `login.html?email=${emailValue}&password=${passwordValue}`;
	} catch (error) {
		alertHint("error", "warning");
	}
});

const togglePassword = document.getElementById("togglePassword");
togglePassword.addEventListener("click", function () {
	handelVisibilityPassword(password, this);
});

const toggleِِConfirmPassword = document.getElementById("toggleConfirm");
toggleِِConfirmPassword.addEventListener("click", function () {
	handelVisibilityPassword(confirmPassword, this);
});

