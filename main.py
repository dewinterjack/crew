from dotenv import load_dotenv
load_dotenv()

from crewai_tools import tool
from crewai import Task, Crew, Process

@tool("Tool Name")
def my_simple_tool(question: str) -> str:
    """Tool description for clarity."""
    # Tool logic here
    return "Tool output"

from crewai import Agent

meta_agent = Agent(
  role='Meta Analyser',
  goal='Get information on the meta for {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Straight to the point"
  ),
  tools=[my_simple_tool],
  allow_delegation=True
)

# Creating a writer agent with custom tools and delegation capability
match_agent = Agent(
  role='Match Analyser',
  goal='Find match data for {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "Straight to the point"
  ),
  tools=[my_simple_tool],
  allow_delegation=False
)

research_task = Task(
  description=(
    "Identify the next big trend in {topic}."
    "Focus on identifying pros and cons and the overall narrative."
    "Your final report should clearly articulate the key points,"
    "its market opportunities, and potential risks."
  ),
  expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
  tools=[my_simple_tool],
  agent=meta_agent,
)

# Writing task with language model configuration
write_task = Task(
  description=(
    "Compose an insightful article on {topic}."
    "Focus on the latest trends and how it's impacting the industry."
    "This article should be easy to understand, engaging, and positive."
  ),
  expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
  tools=[my_simple_tool],
  agent=match_agent,
  async_execution=False,
  output_file='new-blog-post.md'  # Example of output customization
)

crew = Crew(
  agents=[meta_agent, match_agent],
  tasks=[research_task, write_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)