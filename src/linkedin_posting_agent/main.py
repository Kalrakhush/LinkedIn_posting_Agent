#!/usr/bin/env python
import sys
from  src.crew import LinkedInPostingCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        "topic": "Data Science",
        'tone': 'professional',
        "audience": "Data Scientists",
        "details": "This is a post about data science",
        "hashtags": ["#DataScience", "#MachineLearning", "#AI"],
    }
    LinkedInPostingCrew().crew().kickoff(inputs=inputs)
    

if __name__ == "__main__":
    run()