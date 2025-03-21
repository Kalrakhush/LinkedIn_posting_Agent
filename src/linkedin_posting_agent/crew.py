
import os
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

@CrewBase
class LinkedInPostingCrew:
    """Crew to generate and post LinkedIn content."""
    
    # YAML configuration file paths
    agents_config =r"C:\Users\15038\Desktop\LinkedIn_posting_Agent-dev\src\linkedin_posting_agent\config\agents.yaml"
    tasks_config =r"C:\Users\15038\Desktop\LinkedIn_posting_Agent-dev\src\linkedin_posting_agent\config\tasks.yaml"
    
    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            verbose=True
        )
    
    @agent
    def linkedin_poster(self) -> Agent:
        linkedin_tool = LinkedInPostingTool()
        return Agent(
            config=self.agents_config['linkedin_poster'],
            verbose=True,
            tools=[linkedin_tool]
        )
    
    @task
    def create_post_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_post_task']
        )

    @task
    def post_to_linkedin_task(self) -> Task:
        return Task(
            config=self.tasks_config['post_to_linkedin_task']
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,   # Automatically collected via @agent decorators
            tasks=self.tasks,     # Automatically collected via @task decorators
            process=Process.sequential,
            verbose=True,
        )


