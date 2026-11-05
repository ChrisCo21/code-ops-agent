import anthropic

client = anthropic.Anthropic()  # picks up your secret automatically
msg = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "Explain digital code inventory in two sentences."}],
)
print(msg.content[0].text)