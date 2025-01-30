print("Starting")

from ai import llm, embed

prompt = "who landed on the moon"
# or
#prompt = input("Enter Prompt: ")

answer = embed(prompt)

print(answer)
