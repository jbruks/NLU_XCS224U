import lamini
lamini.api_key = "27a088de416ac80c31f04bfe908a3d52da430c130b9b0858b3e1c53bf725b07e"

from torchdynamo.utils import is_torchdynamo_compiling


llm = lamini.Lamini("meta-llama/Llama-2-7b-chat-hf")
print(llm.generate("How are you?"))

#from lamini import LlamaV2Runner

#pirate_llm = LlamaV2Runner(system_prompt="You are a pirate. Say arg matey!")
#print(pirate_llm("How are you?"))
