from crewai import Agent


def create_eligibility_agent(llm):

    return Agent(
        role="Student Eligibility Evaluator",

        goal=(
            "Evaluate the student's academic profile against the admission "
            "requirements identified by the requirements analyst."
        ),

        backstory=(
            "You are an academic eligibility evaluator. "
            "You compare a student's degree, CGPA, skills, experience, "
            "and other information with the identified requirements. "
            "You clearly explain satisfied requirements and possible gaps."
        ),

        llm=llm,

        verbose=True,
        allow_delegation=False
    )
