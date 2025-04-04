import API_CONFIG from "./config.local.js";
async function fetchData() {
    // await Promise.all([loadAccuracyResponse(), loadDataResponse()]);
    loadAccuracyResponse();
    loadDataResponse();
}

async function loadDataResponse() {
    const dataResponse = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.DATA_DISTRIBUTION}`);
    const data = await dataResponse.json();
    createChart("dataDistributionChart", "Review Sentiment Distribution", data);
}

async function loadAccuracyResponse() {
    const accuracyResponse = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ACCURACY_COMPARISON}`);
    const accuracy = await accuracyResponse.json();
    createChart("accuracyComparisonChart", "Model Accuracy Comparison", accuracy);
}

function adjustDropdownHeight() {
    const dropdown = document.getElementById("reviewDropdown");
    const selectedOption = dropdown.options[dropdown.selectedIndex];

    if (!selectedOption) return;

    // Tạo một phần tử ẩn để đo kích thước nội dung
    const tempDiv = document.createElement("div");
    tempDiv.style.position = "absolute";
    tempDiv.style.visibility = "hidden";
    tempDiv.style.whiteSpace = "normal"; // Cho phép xuống dòng
    tempDiv.style.width = dropdown.clientWidth + "px"; // Giới hạn theo dropdown
    tempDiv.style.font = window.getComputedStyle(dropdown).font; // Lấy font của dropdown
    tempDiv.textContent = selectedOption.text; // Gán nội dung cần đo
    document.body.appendChild(tempDiv);

    // Tính toán chiều cao theo nội dung
    const lineHeight = parseFloat(window.getComputedStyle(dropdown).lineHeight) || 20;
    const newHeight = Math.ceil(tempDiv.clientHeight / lineHeight) * lineHeight + 20; // Thêm padding

    document.body.removeChild(tempDiv); // Xóa phần tử ẩn sau khi đo

    dropdown.style.height = Math.min(newHeight, 200) + "px"; // Giới hạn chiều cao tối đa
}
// Gọi hàm khi trang tải hoặc khi dropdown thay đổi
document.addEventListener("DOMContentLoaded", adjustDropdownHeight);
document.getElementById("reviewDropdown").addEventListener("change", adjustDropdownHeight);


function createChart(canvasId, title, data) {
    new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: title,
                data: Object.values(data),
                backgroundColor: ["#FF6384", "#FFCE56", "#36A2EB"]
            }]
        }
    });
}

window.onload = function () {
    fetchData();
};
fetchData();
