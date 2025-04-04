const express = require('express');
const multer = require('multer');
const cors = require('cors');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = 3000;
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const upload = multer({ dest: 'uploads/' });

// API upload file CSV lên backend
app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        const formData = new FormData();
        formData.append('file', req.file);

        const response = await axios.post('http://localhost:8000/upload/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Lỗi upload file!' });
    }
});

// API gửi review để dự đoán
app.post('/predict', async (req, res) => {
    try {
        const response = await axios.post('http://localhost:8000/predict/', req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Lỗi dự đoán!' });
    }
});

app.listen(PORT, () => {
    console.log(`Frontend server chạy tại http://localhost:${PORT}`);
});
