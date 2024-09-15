const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

app.post('/api/predictive-search', async (req, res) => {
    const { query } = req.body;

    // Replace with your Databricks API endpoint and credentials
    const databricksEndpoint = 'https://<databricks-instance>/api/2.0/preview/scoring/models/<model-name>/versions/<version>/predict';
    const databricksToken = 'Bearer <your-databricks-token>';

    try {
        const response = await axios.post(databricksEndpoint, { query }, {
            headers: {
                'Authorization': databricksToken,
                'Content-Type': 'application/json'
            }
        });

        const results = response.data.results; // Adjust based on your Databricks response structure
        res.json({ results });
    } catch (error) {
        console.error("Error fetching predictive search results from Databricks:", error);
        res.status(500).json({ error: 'Failed to fetch predictive search results' });
    }
});

app.listen(5000, () => {
    console.log('Server is running on port 5000');
});