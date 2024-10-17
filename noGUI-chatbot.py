#Rishaud Richard
# Building a very simple Ollama Local Chat Bot using langchain, langchain-ollama and ollama
# This chatbot only stores the history of a single run. If executed again, the previous history will not be available.

from langchain_ollama import OllamaLLM # importing necessary modules
from langchain_core.prompts import ChatPromptTemplate # importing necessary modules


#*Template: This template is passed to the LLM that contains the prompt given. It gives the LLM a better description and instruction on how to respond
    #Answer the Question Below. -> Tells the model to answer the question below
    #Here is the conversation history: {context}  -> providing the LLM with context (Conversation History)

template = """ 
Answer the Question Below.

Here is the conversation history: {context} 

Question: {question}

Answer: 
"""

model = OllamaLLM(model="llama3")                                   #Defines the model used for this chatbot
prompt = ChatPromptTemplate.from_template(template)                 #uses the chatPromptTemplate above (template)
chain = prompt | model                                              #Chains the two operations. The prompt will have the question and the context. Then it'll be passed to the model to be invoked


#* This function allows us to actively talk to the bot while storing conversation history
def conversation():
    context = ""
    print("Welcome to Rishauds AI ChatBot Using Ollama! Type 'exit' to quit.")  #welcome message
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':                                    # if user enters 'exit', break through the loop
            break
        result = chain.invoke({"context": context, "question": user_input}) # provides the LLM with the context as well as the question, where the result is stored in the variabe called "result"
        print("Ollama Bot: ", result)                                       #prints answer of the question
        context += f"\nUser: {user_input}\nAI: {result}"                    #Stores the previous prompt in the context variable, so the bot can use it to respond later on.

if __name__ == "__main__":
    conversation()
