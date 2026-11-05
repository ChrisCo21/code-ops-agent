import anthropic

client = anthropic.Anthropic()  # picks up secret
msg = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    system="You assist a video game publisher's digital operations team. "
           "'Digital codes' means redeemable game keys sold through retailers "
           "and platforms like PlayStation, Xbox and Nintendo.", # Help API Call with defining what Digital Codes are
    messages=[{"role": "user", "content": "Explain digital code inventory in two sentences."}],
)

print(msg.content[0].text)