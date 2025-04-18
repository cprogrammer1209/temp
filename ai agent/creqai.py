from crewai import Agent, Crew, Task
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.tools import Tool
import os

# Set up OpenAI API key (Replace with your key or use env variable)
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Initialize the LLM model (you can use GPT-4 or other LLMs)
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# --- Define AI Tools for Email & Calendar ---

def send_email_tool(to=None, subject=None, body=None):
    """Send an email dynamically by asking for missing details."""
    missing_fields = []
    if not to:
        missing_fields.append("recipient email")
    if not subject:
        missing_fields.append("email subject")
    if not body:
        missing_fields.append("email body")

    if missing_fields:
        return f"Missing details: {', '.join(missing_fields)}. Please provide them."

    print(f"📩 Sending Email to {to}: {subject}\n{body}")
    return "✅ Email Sent Successfully"

def read_email_tool():
    """Fetch and display emails."""
    print("📨 Fetching latest emails...\n")
    return [
        {"from": "boss@example.com", "subject": "Meeting Reminder", "body": "Don't forget our meeting at 3 PM."},
        {"from": "friend@example.com", "subject": "Weekend Plans", "body": "Let's go for a trip this weekend!"}
    ]

def book_event_tool(title=None, date=None, time=None):
    """Book an event dynamically."""
    missing_fields = []
    if not title:
        missing_fields.append("event title")
    if not date:
        missing_fields.append("event date")
    if not time:
        missing_fields.append("event time")

    if missing_fields:
        return f"Missing details: {', '.join(missing_fields)}. Please provide them."

    print(f"📅 Booking Event: {title} on {date} at {time}")
    return "✅ Event Booked Successfully"

def read_calendar_tool():
    """Read calendar events."""
    print("📅 Fetching calendar events...\n")
    return [
        {"title": "Project Meeting", "date": "2025-02-12", "time": "10:00 AM"},
        {"title": "Doctor Appointment", "date": "2025-02-15", "time": "4:00 PM"}
    ]

# --- Define AI Agents ---

email_agent = Agent(
    role="Email Assistant",
    goal="Handle user emails by sending or reading them.",
    tools=[
        Tool(name="Send Email", func=send_email_tool),
        Tool(name="Read Emails", func=read_email_tool)
    ],
    memory=True,
    llm=llm
)

calendar_agent = Agent(
    role="Calendar Assistant",
    goal="Manage user calendar events like booking or reading schedules.",
    tools=[
        Tool(name="Book Event", func=book_event_tool),
        Tool(name="Read Calendar", func=read_calendar_tool)
    ],
    memory=True,
    llm=llm
)

# --- AI Decision-Making Agent (Dynamic Intent Recognition) ---

decision_agent = Agent(
    role="Decision Maker",
    goal="Understand user intent and decide which agent should handle it.",
    memory=True,
    llm=llm
)

# --- Define Dynamic Task Execution ---

def get_user_intent():
    """Ask the user for a natural language request."""
    return input("How can I assist you today? ")

def decide_action(user_input):
    """Ask LLM to decide what to do based on user input."""
    system_prompt = """
    You are an AI assistant that decides the best action based on user input.
    The available tasks are:
    - 'send_email': When the user wants to send an email.
    - 'read_email': When the user wants to check inbox or read emails.
    - 'book_event': When the user wants to schedule a meeting or event.
    - 'read_calendar': When the user wants to check their schedule.

    If the user intent is unclear, ask clarifying questions.
    Respond with ONLY the task name without extra text.
    """

    response = llm([SystemMessage(content=system_prompt), HumanMessage(content=user_input)])
    return response.content.strip()

# --- Main Execution Loop ---

def dynamic_task_runner():
    """Main AI loop for dynamic task execution."""
    user_input = get_user_intent()
    action = decide_action(user_input)

    print(f"🤖 AI Decision: {action}")

    if action == "send_email":
        send_email_tool()
    elif action == "read_email":
        emails = read_email_tool()
        for email in emails:
            print(f"📧 From: {email['from']}\n   Subject: {email['subject']}\n   Body: {email['body']}\n")
    elif action == "book_event":
        book_event_tool()
    elif action == "read_calendar":
        events = read_calendar_tool()
        for event in events:
            print(f"📆 {event['title']} on {event['date']} at {event['time']}")
    else:
        print("🤖 I didn't understand your request. Can you clarify?")

if __name__ == "__main__":
    dynamic_task_runner()
