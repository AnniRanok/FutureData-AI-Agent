# FutureData AI Agent

Welcome to **FutureData AI Agent** 

**FutureData** is a new generation AI assistant for finance teams working with large reporting volumes, data lakes and consolidation systems (eg Oracle HFM, Tagetik, OneStream, SAP BPC).

Instead of manual analysis, downloading Excel files and endless "cleaning" — FutureData automatically processes financial flows, detects anomalies, explains results and predicts risks.

This version represents a **technical draft** on the way to our full AI assistant for finance.  
🔄 **Note:** This is not a final product — but a working base we’re shaping into a full assistant for finance teams.

## Live Demo

 https://github.com/AnniRanok/FutureData-AI-Agent/blob/main/static/videos/future-data.mp4


##  Features (Prototype Preview)

✅ Automatic ingestion of financial data from connected systems  
✅ Natural language interface powered by OpenAI GPT-4  
✅ Python + Pandas code generation for on-the-fly calculations  
✅ AI-generated explanations for KPIs, anomalies, and trends  
✅ Real-time anomaly detection using Z-Score logic  
✅ Auto-generated TODO list with next steps  
✅ Agent activity log showing step-by-step reasoning  
✅ Voice responses using browser-based Web Speech API  
✅ Clean, modular interface (Streamlit/Flask-based)


## Project Structure

<h3>📁 Project Structure</h3>
<pre>
FutureData-AI-Agent/
├── future_data_app/                 # Core application
│   ├── app.py                      # Main logic (OpenAI + Pandas)
│   ├── components/                 # UI components
│   ├── data/                       # Example datasets
│   ├── utils/                      # Helper functions
│   └── requirements.txt            # App dependencies
├── static/                         # Frontend assets
│   ├── js/
│   ├── css/
│   └── videos/
├── templates/
│   └── index.html                  # Landing page
├── app.py                          # Flask / Streamlit entry point
├── main.py                         # Optional CLI / launcher
├── README.md
└── ...
</pre>




## Example Use Case

FutureData is designed for mid to large finance teams using data lakes or financial consolidation software (e.g. Oracle HFM, SAP, Tagetik, OneStream).

Instead of manually uploading spreadsheets, our system connects to your data sources, then:

Automatically ingests and cleans financial data

Detects anomalies, errors, and inconsistencies

Calculates KPIs, metrics, and management ratios

Generates narrative insights, explanations, and visualizations

Prepares reporting summaries and recommendations

Supports multi-entity, multi-language structures

This saves teams hours of validation work and improves reporting quality across the board.


##  Current Status

This repository serves as a **technical draft** of the backend and prototype logic.  
We are building this in preparation for:

📅 **Presentation: June 18, 2025**  
📍 **Nevus50 International Conference**, Luxembourg


## Roadmap (Nevus50 edition)

🔜 Next development stages:

1. Native integration with data consolidation platforms (Oracle, SAP, Tagetik, OneStream)

2. AI-based data reconciliation and report validation

3. Dynamic KPI libraries with customizable rules

4. Forecast generation and scenario planning

5. Automated audit trail and reporting logs

6. Support for multilingual outputs (UI + voice)

7. Email-based summaries and stakeholder briefings

8. Customizable alert logic (thresholds, frequency, audience)


##  Tech Stack

- **OpenAI GPT-4 / GPT-3.5** — core logic and explanations  
- **Pandas + NumPy + Matplotlib** — financial analytics  
- **Scipy (Z-Score)** — anomaly detection  
- **Web Speech API** — browser-based voice feedback  
- **Streamlit / Flask** — interactive UI and dashboard logic  
- **Optional integrations:** FPDF, LangChain, Postgres, Airbyte



## Built by
Future Data team — turning spreadsheets into smart systems with the help of AI.



## Contact

Got feedback or ideas?  
📧 konar.inna@gmail.com  
🌐 Website: https://futuredata-ai.netlify.app/  

