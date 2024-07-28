document.addEventListener("click", function (event) {
	if (event.target.classList.contains("signOutBtn")) {
		signOut();
	}
});
const detectContainer = document.querySelector(".detailsContainer");
const pressionBox = document.querySelector(".pression");
const debit = document.querySelector(".debit");
const statBtn = document.querySelector(".statBtn");

const arrAnomaly = [
	{
		pressure: "3.4",
		flow: "1.2",
	},
	{
		pressure: "4.1",
		flow: "0.9",
	},
	{
		pressure: "3.9",
		flow: "1.4",
	},
	{
		pressure: "4.2",
		flow: "1.0",
	},
	{
		pressure: "3.5",
		flow: "1.3",
	},
	{
		pressure: "4.0",
		flow: "1.1",
	},
	{
		pressure: "3.7",
		flow: "1.2",
	},
	{
		pressure: "4.3",
		flow: "1.5",
	},
	{
		pressure: "3.6",
		flow: "1.0",
	},
	{
		pressure: "4.4",
		flow: "1.6",
	},
];

function changePressionDom(pressure) {
	pressionBox.innerHTML = `<h2>${pressure}<span>Pa</span></h2>
					<p>pression actuelle</p>`;
}
function changeDebitDom(value) {
	debit.innerHTML = `			<h2>${value} <span>m³/minute</span></h2>
					<p>débit actuel</p>`;
}
function changeStatBtnDom(anomaly) {
	statBtn.textContent = anomaly ? "on" : "off";
}

async function getPredictResponse(pressure, flow) {
	try {
		token = localStorage.getItem("token");
		const response = await axios.post(
			`${baseUrl}/predict`,
			{
				pressure: pressure,
				flow: flow,
			},
			{
				headers: {
					Authorization: `Bearer ${token}`,
				},
			}
		);

		const data = response.data;

		return data.anomaly;
	} catch (error) {
		// Handle error and display message
		if (error.response && error.response.data && error.response.data.error) {
			throw { message: error.response.data.error, type: "warning" };
		} else {
			console.log(error);
			throw { message: "An unexpected error occurred.", type: "danger" };
		}
	}
}

function getHtmlResponse(anomalyStat) {
	if (anomalyStat) {
		detectContainer.classList.add("remove");
		return `<div class="leftContent">
				<p class="detailsDate">${new Date()}</p>

			<p class="detailsDescription">Il y a une fuite dans votre système d'eau. Veuillez vérifier vos canalisations et robinets pour identifier et réparer la source de la fuite afin d'éviter des dégâts supplémentaires et des factures d'eau élevées.</p>

			</div>

			<div class="rightContent">
				<img src="imgs/distIcon.png" alt="" />
				<span class="detailsDistance">distance</span>
				<p class="detailsDistanceValue">100m</p>
			</div>`;
	}
	detectContainer.classList.add("disable");
	return "";
}

async function manageAlertAnomaly(pressure, flow) {
	try {
		let anomaly = await getPredictResponse(pressure, flow);
		detectContainer.innerHTML = getHtmlResponse(anomaly);
		changeStatBtnDom(anomaly);
		console.log(pressure);
		changePressionDom(pressure);
		changeDebitDom(flow);
	} catch (error) {
		alertHint(error.message, error.type);
	}
}

window.addEventListener("load", async function () {
	for (anomalyInfo of arrAnomaly) {
		await manageAlertAnomaly(anomalyInfo.pressure, anomalyInfo.flow);
		await wait(10 * 1000);
		await alertHint("Update", "success");
	}
});
