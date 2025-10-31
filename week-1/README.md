# Week1
Ok so in week1 we mostly focused on setting the environments on our systems. Such as Installing Jupyter notebook and Jupyter lab, then also using Google collab. we are going to sometimes run the models on Google Collab servers as it is easily accessible to everyone of the gorup.

But sometimes when on the cloud server if the ram and cpu reaches its limit then we will have no choice but to run it locally using Jupyter Lab and share the updates on GitHub.

We installed matploit, Hugging Face transformers, torch(transformer backend which is installed automatically), matplotlib(To later graph the data of the results which we get), langchain (for automation, chaining of tasks, integration of external tools), and pandas for data manipulation and analysis.

# HuggingFace(transformers) & pipeline
We load (import) a helper called pipeline from the transformers library so you can use it in your code.

'transformers' is the name of a Python package (library) made by Hugging Face. It contains pre-built code to download and use many language models easily.

Pipeling is the specific tool/function inside transformers that wraps model loading, tokenization, and text generation into one easy-to-use object.

# Tokens
Tokens are named parameter telling the generator to produce at most 100 new tokens (tokens are pieces of text; a token is roughly a word or part of a word). And then the output is generated in a list and the output value is under the key 'generated_text'.

# do_Sample=True
It makes the model pick from a distribution of possible next tokens randomly (according to probabilities), leading to diverse outputs. If False, the model picks the highest-probability next token at every step (deterministic).
