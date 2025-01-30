print("Starting")

from ai import llm

prompt = "who landed on the moon"
# or
#prompt = input("Enter Prompt: ")

answer = llm(prompt)

print(answer)