const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static("public")); // Serve frontend files
const PORT = 3000;
app.listen(PORT, () => {console.log(`Frontend server running at http://localhost:${PORT}`);
});