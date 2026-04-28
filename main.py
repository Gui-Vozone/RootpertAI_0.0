from openai import OpenAI

# Create client (uses OPENAI_API_KEY from environment)
client = OpenAI()


def chat_with_gpt(messages):
    """
    messages: list of dicts like:
    [{"role": "user", "content": "Hello"}]
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages
    )

    return response.output_text


# Optional: terminal testing mode
if __name__ == "__main__":
    conversation = []

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        conversation.append({
            "role": "user",
            "content": user_input
        })

        reply = chat_with_gpt(conversation)

        print("Chatbot:", reply)

        conversation.append({
            "role": "assistant",
            "content": reply
        })