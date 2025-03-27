
import os
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from linkedin_api import Linkedin

# Load environment variables from .env
load_dotenv()

@CrewBase
class LinkedInPostingCrew:
    """Crew to generate and post LinkedIn content."""
    
    # YAML configuration file paths
    agents_config = "src/linkedin_posting_agent/config/agents.yaml"
    tasks_config = "src/linkedin_posting_agent/config/tasks.yaml"
    
    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['content_creator'],
            verbose=True
        )
    
    @agent
    def linkedin_poster(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_poster'],
            verbose=True
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

def post_on_linkedin(post_content: str) -> str:
    """
    Uses linkedin-api to post a share on LinkedIn.
    """
    username = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    if not username or not password:
        raise ValueError("LinkedIn credentials are not set in the .env file")
    try:
        # Log in using your personal LinkedIn account credentials.
        api = Linkedin(username, password)
        # Submit the post. Adjust parameters as needed.
        response = api.submit_share(post_content)
        return "LinkedIn post submitted successfully."
    except Exception as e:
        return f"Error posting on LinkedIn: {str(e)}"
