# Steps to run the python agent demo
- Create virtualenv using command `python3 -m venv venv`
- Activate virtualenv using command `source venv/bin/activate`
- Install the libraries using command `pip3 install -r requirements.txt`
- Setup your .env file
  ´
  OPENAI_API_KEY="your-api-key" #required variable
  TAVILY_API_KEY_SID="your-tavily-api-key"
  ´
- To run the project use the command `uvicorn main:app --reload`