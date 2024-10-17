import sys
from langchain_ollama import OllamaLLM  # Importing necessary modules
from langchain_core.prompts import ChatPromptTemplate  # Importing necessary modules
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QColor, QTextCursor, QPalette  # Ensure QPalette is imported

#*Template: This template is passed to the LLM that contains the prompt given. It gives the LLM a better description and instruction on how to respond
    #Answer the Question Below. -> Tells the model to answer the question below
    #Here is the conversation history: {context}  -> providing the LLM with context (Conversation History)
template = """ 
Answer the Question Below.

Here is the conversation history: {context} 

Question: {question}

Answer: 
"""

model = OllamaLLM(model="llama3")  # Defines the model used for this chatbot
prompt = ChatPromptTemplate.from_template(template)  # Uses the chatPromptTemplate above (template)
chain = prompt | model  # Chains the two operations

class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.context = ""

    def initUI(self):
        self.setWindowTitle("Rishaud's AI ChatBot Using Ollama")
        self.setGeometry(100, 100, 400, 500)

        # Set the main window gradient background
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient_color = QPalette()
        gradient_color.setColor(QPalette.Window, QColor(128, 0, 128))  # Dark Purple
        self.setPalette(gradient_color)

        self.layout = QVBoxLayout()

        # Chat area with gradient background
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)

        # Set gradient background using style sheet
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                             stop: 0 rgba(100, 0, 255, 255), 
                                             stop: 1 rgba(150, 100, 255, 255));
                color: white;  /* Default text color for the bot's response */
            }
        """)

        self.layout.addWidget(self.chat_area)

        # User input
        self.user_input = QLineEdit(self)
        self.layout.addWidget(self.user_input)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Bind the Enter key to send the message
        self.user_input.returnPressed.connect(self.send_message)

        self.setLayout(self.layout)

    def send_message(self):
        user_text = self.user_input.text()
        if user_text.lower() == 'exit':
            QApplication.quit()  # Exit the application if user types 'exit'

        # Invoke the chatbot with the current context and user input
        result = chain.invoke({"context": self.context, "question": user_text})

        # Append user input and bot response to the chat area with specified colors
        self.chat_area.append(f"<font color='red'>You:</font> <font color='white'>{user_text}</font>")  # User's header in red, text in white
        self.chat_area.append(f"<font color='yellow'>Ollama Bot:</font> <font color='white'>{result}</font>\n")  # Bot's header in yellow, text in white

        # Update context for the next interaction
        self.context += f"\nUser: {user_text}\nAI: {result}"

        # Clear the input field
        self.user_input.clear()

        # Ensure the chat area is scrolled to the bottom
        self.chat_area.moveCursor(QTextCursor.End)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatBotApp()
    ex.show()
    sys.exit(app.exec_())
