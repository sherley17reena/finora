from app.database import SessionLocal
from app.models import AgentLog


db = SessionLocal()

try:
    logs = db.query(AgentLog).all()

    print("=== ALL AGENT LOGS ===")

    for log in logs:
        print("\nLog ID:", log.id)
        print("Agent:", log.agent)
        print("Action:", log.action)
        print("Tool:", log.tool)
        print("Arguments:", log.arguments)
        print("Result:", log.result)
        print("Timestamp:", log.timestamp)

finally:
    db.close()