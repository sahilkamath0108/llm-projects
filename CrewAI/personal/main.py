import os
from crewai import Agent, Crew, Task, Process
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["OPENAI_API_BASE"]='http://localhost:1234/v1'
os.environ["OPENAI_MODEL_NAME"]='codellama'
os.environ["OPENAI_API_KEY"]='not-needed'

llm = ChatGoogleGenerativeAI(
    model="gemini-pro", verbose=True, temperature=0.2, google_api_key=''
)

def create_code(code):
    coder = Agent(
    role="Software Developer",
    goal='Write neat and clean code for whatever problem statement has been provided to you.',
    backstory="""You are a software developer. You have been tasked with writing some code that will make your team's life easier.""",
    verbose=True,
    llm= llm
    )
    
    supervisor = Agent(
        role="Project Manager",
        goal="Ensure that the code developed by Software Developer/ Coder is of high quality.",
        backstory="""You are a project manager. You have been tasked with ensuring that the code developed by Software Developer/ Coder is of high quality.""",
        verbose=True, 
        allow_delegation=True, 
        llm= llm
    )
    
    task1 = Task(
        description = f'Write a robust and efficient code for {code}',
        agent= coder
    )
    
    task2 = Task(
        description= """Check if the code written by another developer meets the standards of a good and clean code. If not instruct the agent
        on how to improve it. 
        """,
        agent=supervisor,
    )
    
    crew = Crew(
    agents=[coder, supervisor],
    tasks=[task1, task2],
    verbose=2,
    process=Process.sequential,  
    )
    
    result = crew.kickoff()

    print("######################")
    print(result)
    
    
if '__main__' == __name__:
    subject = input("Enter the subject: ")
    create_code(subject)