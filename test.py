print("Starting")


from ai_embedding import embed

text = "apple"
print(f"The test: {text}")
embedding = embed(text)

print(embedding)
