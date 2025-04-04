function getCSRFToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];

    return cookieValue || "";
}


async function predictReview() {
    const review = document.getElementById("reviewText").value;
    const model = document.getElementById("modelType").value;

    const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" ,
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ review, model })
    });

    const data = await response.json();
    document.getElementById("result").innerText = "Dự đoán: " + data.prediction;
}

// Giả lập dữ liệu thống kê
const dataDistribution = {
    labels: ["Negative", "Neutral", "Positive"],
    datasets: [{
        label: "Phân bố review",
        data: [30, 40, 30],
        backgroundColor: ["red", "yellow", "green"]
    }]
};

const accuracyComparison = {
    labels: ["CNN", "RNN", "LSTM"],
    datasets: [{
        label: "Độ chính xác",
        data: [85, 80, 88],
        backgroundColor: ["blue", "purple", "orange"]
    }]
};

new Chart(document.getElementById("dataChart"), { type: "pie", data: dataDistribution });
new Chart(document.getElementById("accuracyChart"), { type: "bar", data: accuracyComparison });
