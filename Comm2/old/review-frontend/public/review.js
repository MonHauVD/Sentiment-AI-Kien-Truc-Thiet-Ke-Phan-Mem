function getCSRFToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];

    return cookieValue || "";
}

async function uploadCSV() {
    const fileInput = document.getElementById("csvFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Vui lòng chọn file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // const response = await fetch("/upload", { method: "POST", body: formData });
    // Lấy token CSRF từ cookie
    // const csrfToken = getCookie("csrftoken");

    const response = await fetch("/upload", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(), // Gửi token CSRF trong header
        },
    });
    const data = await response.json();
    document.getElementById("uploadMessage").innerText = data.message;
}

// Lấy danh sách review từ backend
async function loadReviews() {
    const response = await fetch("http://localhost:8000/reviews");
    const data = await response.json();
    
    const reviewList = document.getElementById("reviewList");
    reviewList.innerHTML = "";
    data.forEach(review => {
        const li = document.createElement("li");
        li.textContent = `${review.reviewer_name}: ${review.summary} (Rating: ${review.rating})`;
        reviewList.appendChild(li);
    });
}

window.onload = loadReviews;
