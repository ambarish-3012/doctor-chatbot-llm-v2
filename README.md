# 🩺 Doctor Appointment Chatbot with LLM (OpenAI + Streamlit)

Welcome to the **Super Clinic AI Chatbot**, an intelligent doctor appointment system powered by OpenAI function calling, MySQL database integration, and a clean Streamlit-based UI.

This project demonstrates how a production-grade chatbot can use LLMs to interpret natural language, understand medical queries, and perform real-time actions like checking doctor availability and booking appointments.

---

## 🚀 Features

- 🤖 Conversational chatbot using OpenAI GPT with Function Calling
- 🏥 Suggests departments based on user symptoms
- 👩‍⚕️ Lists available doctors by department
- 📅 Checks doctor availability
- ✅ Books confirmed appointments
- 💻 Built with Python, MySQL, and Streamlit

---

## 📁 Project Structure

```bash
doctor-chatbot-llm-v2/
│
├── app.py                    # Streamlit UI
├── openai_api.py            # Core OpenAI function-calling logic
├── functions.py             # Tool functions called by the LLM
├── database_connection.py   # MySQL connector
├── prompt_system.py         # System prompt for chatbot behavior
├── requirements.txt         # Python dependencies
├── .env                     # Contains OpenAI API key (excluded via .gitignore)
└── .gitignore


🛠️ Setup Instructions

1) Clone the repository

git clone https://github.com/ambarish-3012/doctor-chatbot-llm-v2.git
cd doctor-chatbot-llm-v2

2) Create and activate a virtual environment (Anaconda recommended)

conda create -n doctor_chatbot python=3.11
conda activate doctor_chatbot

3) Install dependencies

pip install -r requirements.txt

4) Configure environment

Create a .env file in the root folder:
  OPENAI_API_KEY=your_openai_key_here

**Important Note: Never commit .env or expose your API key.

🧪 Run the Project

➤ Option 1: Command Line Chatbot

              python openai_api.py

➤ Option 2: Streamlit Web UI

              streamlit run app.py

🗄️ MySQL Database Setup

Make sure your MySQL server is running and has the following tables:

Table: doctors

CREATE TABLE doctors (
    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_name VARCHAR(255),
    specialization VARCHAR(255),
    department VARCHAR(255)
);

Table: availability

CREATE TABLE availability (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT,
    available_date DATE,
    available_time TIME,
    is_booked TINYINT(1) DEFAULT 0
);

Insert sample data for testing (adjust dates accordingly).

🤝 Contributions
If you find this project helpful or would like to collaborate, feel free to submit a pull request or open an issue.

📜 License
This project is open-source under the MIT License.

👨‍💻 Developed by
Ambarish Chakraborty
https://www.linkedin.com/in/ambarish-chakraborty-38a2b133/
