
# 2023 Canadian Census – Employment Analytics Dashboard

This project is an interactive web-based dashboard developed using Python and Dash. It visualizes employment data derived from the 2023 Canadian Census and is designed to assist federal and provincial policymakers, workforce analysts, and researchers in evaluating labor distribution across Canada.

The dashboard includes interactive visualizations that explore employment trends across provinces and territories, disaggregated by occupational classification and gender. It also provides tools for workforce readiness assessments based on threshold-based filters and proportional analysis.

---

## Key Features

### 1. Essential Worker Distribution (Normalized and Raw)

This bar chart shows the geographic distribution of essential service workers (health, trades, and government services) across Canada's provinces and territories. Users can toggle between raw totals and normalized counts per 1,000 residents to account for population differences. This supports equitable workforce planning and the identification of under-resourced regions.

### 2. Gender Distribution by Occupation

An interactive butterfly chart (population pyramid style) allows users to view male and female employment levels for each occupation within a selected province or territory. Users can choose to view both genders or isolate either male or female employment patterns. This visualization is useful for identifying occupational gender imbalances and supporting equity initiatives.

### 3. Occupation Manpower Threshold Filter

This horizontal bar chart helps users identify which occupations surpass a customizable employment threshold across the country. This feature is particularly relevant for evaluating labor availability in support of new infrastructure or industrial projects (e.g., electric vehicle manufacturing), where a minimum skilled labor force is required.

### 4. Occupational Composition Analysis

This donut chart illustrates the distribution of employment across major occupational categories (based on the National Occupational Classification system) at either the national or provincial level. It provides a high-level overview of workforce structure, highlighting dominant sectors within each administrative unit.

---

## Technologies Used

- **Python 3**
- **Dash** – A Python framework for building analytical web applications
- **Plotly** – Interactive graphing library
- **Pandas** – Data manipulation and analysis library

---

## Running the Application Locally

1. **Clone this repository**
```bash
git clone https://github.com/your-username/employment-dashboard.git
cd employment-dashboard
```

2. **(Optional) Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the application**
```bash
python employment_dashboard.py
```

5. Open your browser and navigate to `http://localhost:8050`

---

## Deployment on Render

To deploy this dashboard online using [Render](https://render.com), follow these steps:

1. Push this project to a public GitHub repository.
2. Create a new **Web Service** on Render.
3. Connect your GitHub repository to Render.
4. Set the following configurations:
   - **Environment**: Python
   - **Start Command**: `python employment_dashboard.py`
   - **Build Command**: (optional) `pip install -r requirements.txt`
5. Select the **Free Plan** (suitable for prototypes and low-traffic apps).
6. Deploy the service. Render will provide a live public URL.

Ensure that `cleaned_data.csv` is included in your repository and referenced locally in the script.

---

## Repository Structure

```
employment-dashboard/
│
├── employment_dashboard.py     # Main Dash application
├── cleaned_data.csv            # Pre-processed census dataset
├── requirements.txt            # Required Python packages
├── render.yaml (optional)      # Deployment configuration for Render
└── README.md                   # Project documentation
```

---

## Author

**Robin Shah**  
Honours Bachelor of Science in Computer Science  
Wilfrid Laurier University  
Email: [your-email@example.com]  
LinkedIn: [your-linkedin-url]

---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software with appropriate attribution.
