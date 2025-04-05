import os
from openai import OpenAI
from dotenv import load_dotenv
from functions import list_doctors_by_department, get_doctor_availability, book_appointment

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store conversation state
messages = []

# Register tools for function calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_doctors_by_department",
            "description": "Get list of doctors by department",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "The department name, e.g., Cardiology"
                    }
                },
                "required": ["department"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctor_availability",
            "description": "Get availability for a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string",
                        "description": "Full name of the doctor"
                    }
                },
                "required": ["doctor_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment with a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string",
                        "format": "date"
                    },
                    "time": {
                        "type": "string"
                    }
                },
                "required": ["doctor_name", "date", "time"]
            }
        }
    }
]

# Tool mapping
available_functions = {
    "list_doctors_by_department": list_doctors_by_department,
    "get_doctor_availability": get_doctor_availability,
    "book_appointment": book_appointment
}

# Start conversation
print("Chatbot: Hello! Welcome to the Super Clinic.")

def chat_with_openai(user_input):
    messages.append({"role": "user", "content": user_input})

    # Step 1: send user message to OpenAI with tool list
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    # Step 2: if tool_call is triggered
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = tool_call.function.arguments

            import json
            arguments = json.loads(function_args)

            print(f"[Debug] Calling function: {function_name} with args: {arguments}")

            function_to_call = available_functions.get(function_name)
            function_response = function_to_call(**arguments)

            # Add tool response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": function_response
            })

        # Step 3: Ask LLM how to respond with tool output
        follow_up = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        follow_up_message = follow_up.choices[0].message
        messages.append(follow_up_message)
        return follow_up_message.content
    else:
        return response_message.content


# Run loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Take care! Goodbye.")
        break

    reply = chat_with_openai(user_input)
    print(f"Chatbot: {reply}")
