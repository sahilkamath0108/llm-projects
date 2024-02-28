from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI


# agent = create_csv_agent(
#     ChatOpenAI(base_url="http://localhost:1234/v1", api_key="not-needed"),
#     "C:\\Users\\Hp\\Desktop\\archive\\tested.csv",
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )

# agent.invoke('Sex of passenger Kelly, Mr. James')


# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

completion = client.chat.completions.create(
  model="local-model", # this field is currently unused
  messages=[
    {"role": "system", "content": "You are a expert coder, and give concise code to every question asked"},
    {"role": "user", "content": "Give code to finetune a llm model on my csv"}
  ],
  temperature=0.7,
)

print(completion.choices[0].message)