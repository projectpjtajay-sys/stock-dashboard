from mcp_client import MCPClient
from outlook_mcp import OutlookMCPClient
from email_service import send_email

USER_CONTEXT_MCP = "http://localhost:8000"
OUTLOOK_MCP = "http://localhost:9000"

def format_schedule(events):
    summary = "Your upcoming schedule:\n\n"
    for event in events:
        summary += (
            f"- {event['subject']}\n"
            f"  From: {event['start']} To: {event['end']}\n\n"
        )
    return summary

def main():
    # Initialize clients
    mcp_client = MCPClient(USER_CONTEXT_MCP)
    outlook_client = OutlookMCPClient(OUTLOOK_MCP)

    # Fetch user context
    user_context = mcp_client.get_user_context()
    user_email = user_context["email"]

    # Fetch calendar events
    events = outlook_client.get_upcoming_events(user_email)

    # Send notification email
    email_content = format_schedule(events)
    send_email(user_email, email_content)

if __name__ == "__main__":
    main()
