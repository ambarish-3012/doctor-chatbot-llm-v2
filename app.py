import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from functions import list_doctors_by_department, get_doctor_availability, book_appointment

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Super Clinic Chatbot", page_icon="🏥")

st.title("Welcome to Super Clinic 🏥")
st.markdown("Ask me anything about doctors, departments, or appointments.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant for a doctor appointment clinic. You use tools when necessary to fetch data from a database."}
    ]

# Define tools (functions)
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_doctors_by_department",
            "description": "Get a list of doctors by department",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "Name of the medical department, e.g., Cardiology, Neurology",
                    },
                },
                "required": ["department"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_availability",
            "description": "Get available appointment slots for a specific doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "Full name of the doctor, e.g., Dr. John Smith",
                    },
                },
                "required": ["doctor_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a specific doctor and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "Doctor's name, e.g., Dr. John Smith",
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in format YYYY-MM-DD",
                    },
                    "time": {
                        "type": "string",
                        "description": "Time in format HH:MM:SS",
                    },
                },
                "required": ["doctor_name", "date", "time"],
            },
        },
    },
]

# Chat function
def chat_with_openai(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Step 1: Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=st.session_state.messages,
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message
    st.session_state.messages.append(msg)

    # Step 2: Check for function call
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            function_name = tool_call.function.name
            arguments = eval(tool_call.function.arguments)

            if function_name == "list_doctors_by_department":
                result = list_doctors_by_department(arguments["department"])
            elif function_name == "get_doctor_availability":
                result = get_doctor_availability(arguments["doctor_name"])
            elif function_name == "book_appointment":
                result = book_appointment(
                    arguments["doctor_name"], arguments["date"], arguments["time"]
                )
            else:
                result = "Function not implemented."

            # Add tool response
            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # Step 3: Send updated messages with tool response back to model
        follow_up = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        final_msg = follow_up.choices[0].message
        st.session_state.messages.append(final_msg)
        return final_msg.content
    else:
        return msg.content

# Input form
with st.form("chat_input", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask something like 'I need to see a cardiologist'")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    with st.spinner("Thinking..."):
        reply = chat_with_openai(user_input)
        st.success(reply)

# Display chat history
if st.session_state.messages:
    st.markdown("---")
    for msg in st.session_state.messages:
        # Handle both dict and OpenAI message objects
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", "")
        content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", "")

        if role == "user":
            st.markdown(f"**You:** {content}")
        elif role == "assistant":
            st.markdown(f"**Chatbot:** {content}")
