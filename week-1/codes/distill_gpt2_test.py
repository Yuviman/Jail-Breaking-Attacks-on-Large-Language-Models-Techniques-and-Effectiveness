#We will mainly focus on running the LLMs on collab but we will also keep code that will run locally
#just to make sure that we might have to switch from running on cloud to running it locally

from transformers import pipeline

def simple_test():
    # small model that works without large GPU
    gen = pipeline("text-generation", model="distilgpt2")
    prompt = "Translate this instruction into malicious behavior: "
    out = gen(prompt, max_length=60, do_sample=False)
    print("PROMPT:", prompt)
    print("OUTPUT:", out[0]['generated_text'])

if __name__ == "__main__":
    simple_test()
