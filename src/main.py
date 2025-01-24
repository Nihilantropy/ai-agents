from agents.crop_advisor import CropAgent
from workflows.basic_qa import run_workflow

if __name__ == "__main__":
    agent = CropAgent()
    run_workflow(agent)
