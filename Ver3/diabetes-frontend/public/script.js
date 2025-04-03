document.getElementById("predictionForm").addEventListener("submit", async function (event)
{
    event.preventDefault();
    let formData = new FormData(event.target);
    let inputValues = Object.fromEntries(formData.entries());
    // Convert values to float
    let features = Object.values(inputValues).map(Number);
    // Send data to Flask API
    let response = await fetch("http://12️7.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: features })
    });
    let result = await response.json();
    document.getElementById("result").innerText = "Prediction: " + result.prediction;
});