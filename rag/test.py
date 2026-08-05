from retriever import retrieve

query = "Tell me about your FastAPI experience"

context = retrieve(query)

print(context)