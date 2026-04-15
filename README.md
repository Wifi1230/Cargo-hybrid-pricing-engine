# 🚛 Cargo-Hybrid-Pricing-Engine (ML)

An intelligent freight rate estimation system powered by Machine Learning. Unlike traditional calculators, this engine predicts optimal market margins based on seasonality, distance, and current operating costs.

## 🚀 Key Features
* **Predictive Margin Engine:** XGBoost-based model estimating profit margins (MAE: ~2.97%).
* **Hybrid Pricing Logic:** Combines "hard" operational costs with AI-driven market intuition.
* **Real-time Data:** Integrated with `yfinance` to fetch live fuel price estimations (Brent Oil).
* **Inflation-Resistant:** Easily update driver rates and maintenance costs without retraining the model.
* **Dynamic Price Brackets:** Provides Min/Suggested/Max pricing with a +/- 3% safety margin.

## 🛠️ Model Insights
The **XGBoost Regressor** analyzes three primary features to determine the target margin:
1.  **Distance:** Impact on per-km profitability.
2.  **Month:** Capturing seasonal peaks (e.g., Q4 holiday rush).
3.  **Day of Week:** Market demand fluctuations during the week.

### Training Performance:
* **Mean Absolute Error (MAE):** 2.97%
* **R2 Score:** 78.36%

## 📂 Project Structure
* `data_generator.py`: Generates synthetic historical data with embedded cost logic.
* `train_model.py`: Trains the XGBoost regressor and exports the `.pkl` model.
* `cargo_calculator.py`: Production-ready inference script for live quotes.
* `Dockerfile`: Containerization setup for easy deployment.

## 🐳 Running with Docker

1.  **Build the image:**
    ```bash
    docker build -t cargo-ml-engine .
    ```

2.  **Run the calculator:**
    ```bash
    docker run -it cargo-ml-engine
    ```

## ⚙️ Manual Installation
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Generate data and train the model:
    ```bash
    python data_generator.py
    python train_model.py
    ```
3.  Run the calculator:
    ```bash
    python cargo_calculator.py
    ```

## 📈 Roadmap
- [ ] Streamlit Dashboard for a web-based UI.
- [ ] Support for multiple vehicle types (Truck, Van, Reefer).