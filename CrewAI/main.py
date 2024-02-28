import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_openai import ChatOpenAI

search = DuckDuckGoSearchResults()

# lm_studio = ChatOpenAI(
#     openai_api_base = 'http://localhost:1234/v1',
#     api_key = 'not-needed',
#     model_name = 'zephyr'
# )
os.environ["OPENAI_API_BASE"]='http://localhost:1234/v1'
os.environ["OPENAI_MODEL_NAME"]='zephyr'
os.environ["OPENAI_API_KEY"]='not-needed'

#Agents

scraper = Agent(
    role='Summarizer of websites',
    goal = 'Ask the user for a list of URLs, then go to each given website, scrape the content, and provide full content to writer agent',
    backstory = """You work at a leading tech think tank.
    Your expertise lies in taking urls and getting text-based content of them.
    """,
    verbose= 'True',
    tools=[search],
    # llm= lm_studio
)

writer = Agent(
    role='Tech Content Summarizer and Writer',
    goal = 'Craft compelling short-form content on AI advancements based on long-form text passed to you.',
    backstory = """
    You are a renowned Content Creator known for your ability to craft compelling short-form content on AI advancements.
    """,
    verbose= 'True',
    allow_delegation=True
)

#Tasks
task1 = Task(
    description= """
    Take a list of websites that contain AI content, read/scrape the content, and then pass
    to writer agent.
    """,
    agent=scraper,
)

task2 = Task(
    description="""
    Using the text provided by the scraper agent, craft a short-form content on AI advancements.
    """,
    agent=writer,
)

#Crew
tech_crew = Crew(
    agents= [scraper, writer],
    tasks = [task1, task2],
    verbose=2
)

res = tech_crew.kickoff()
print(res)