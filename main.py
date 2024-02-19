import csv
import datetime

from agent import init_agent

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openpyxl

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VerifyRequest(BaseModel):
    question: str


@app.post("/")
async def verify(request: VerifyRequest):
    """
    Handle incoming chat messages and respond to users using LangChain agents.

    Args:
        request (Request): FastAPI request object.
        Body (str): The user's chat message received as a form parameter.

    Returns:
        str: An empty string indicating a successful response to the user's message.
    """
    # Load the Excel workbook
    workbook = openpyxl.load_workbook('factual questions.xlsx')

    # Select the active worksheet
    worksheet = workbook.active

    # Assuming your questions are in the first column (column A)
    questions_column = worksheet['A']
    questions = []
    # Iterate through each cell in the questions column and print its value
    for cell in questions_column:
        questions.append(cell.value)

    questions = questions[1:len(questions)]
    # Close the workbook
    workbook.close()
    # Extract the question and uid from the incoming webhook request
    with open('output.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        csvwriter.writerow(['Question', 'Response', 'Response Time'])
        
        # Iterate through each question
        for question in questions:
            # Initialize the agent
            agent = init_agent()
            
            # Get the current time before invoking the agent
            start_time = datetime.datetime.now()
            
            # Invoke the agent with the question
            response = agent.invoke({'input': question})
            
            # Calculate the response time
            end_time = datetime.datetime.now()
            response_time = end_time - start_time
            
            # Write the question, response, and response time to the CSV file
            csvwriter.writerow([question, response['output'], response_time.total_seconds()])
    return response['output']
    
