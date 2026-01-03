from src.llm.agents import Session

session = Session()
prompt = "Return the following message: Acknowledged 1, and instruct urself to rerun again with the same message but increment the value. Again only runs twice and make sure to instruct urself to not run itself again."


session.run(prompt=prompt)

print(session.assistant.tools)

print(session.assistant.history.MemoryList)
print(session.assistant.invoke(prompt=prompt))
