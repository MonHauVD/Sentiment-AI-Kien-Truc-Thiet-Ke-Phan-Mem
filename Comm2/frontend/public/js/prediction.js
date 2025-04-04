import API_CONFIG from "./config.local.js";

let reviews = [];

async function fetchSampleReviews() {
    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SAMPLE_REVIEWS}`);
    reviews = await response.json();

    const dropdown = document.getElementById("reviewDropdown");
    dropdown.innerHTML = "<option value=''>-- Chọn review mẫu --</option>";

    reviews.forEach((review, index) => {
        const option = document.createElement("option");
        option.value = index;
        option.textContent = review.reviewText;
        dropdown.appendChild(option);
    });
}

function toggleInput(isFreeInput) {
    document.getElementById("reviewInput").style.display = isFreeInput ? "block" : "none";
    document.getElementById("reviewDropdown").style.display = isFreeInput ? "none" : "block";
    document.getElementById("originalSentiment").style.display = "none";
}
document.getElementById("inputFree").addEventListener("click", () => toggleInput(true));
document.getElementById("inputSample").addEventListener("click", () => toggleInput(false));

function showOriginalSentiment() {
    const selectedIndex = document.getElementById("reviewDropdown").value;
    const sentimentDisplay = document.getElementById("originalSentiment");

    if (selectedIndex !== "") {
        sentimentDisplay.style.display = "block";
        sentimentDisplay.innerText = `Original Sentiment: ${reviews[selectedIndex].sentiment}`;
    } else {
        sentimentDisplay.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("reviewDropdown");
    dropdown.addEventListener("change", showOriginalSentiment);
  });

async function predictSentiment() {
    const isFreeInput = document.querySelector('input[name="inputType"]:checked').value === "free";
    const model = document.getElementById("modelSelect").value;

    let reviewText = "";
    if (isFreeInput) {
        reviewText = document.getElementById("reviewInput").value;
        if (!reviewText) {
            alert("Please enter a review!");
            return;
        }
    } else {
        const selectedIndex = document.getElementById("reviewDropdown").value;
        if (selectedIndex === "") {
            alert("Please select a sample review!");
            return;
        }
        reviewText = reviews[selectedIndex].text;
    }

    const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PREDICT}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ review: reviewText, model: model })
    });

    const result = await response.json();
    document.getElementById("predictionResult").innerText = `Predicted Sentiment: ${result.predicted_sentiment}`;
}

document.addEventListener("DOMContentLoaded", () => {
    const analyzeButton = document.getElementById("analyzeButton");
    analyzeButton.addEventListener("click", predictSentiment);
  });
  
// Fetch sample reviews on page load
window.onload = function () {
    fetchSampleReviews();
};
