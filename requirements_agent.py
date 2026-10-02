from crewai import Agent


def create_requirements_agent(llm):

    return Agent(
        role="Admission Requirements Analyst",

        goal=(
            "Analyze the student's requested degree and field and identify "
            "the relevant admission requirements."
        ),

        backstory=(
            "You are an admission requirements specialist. "
            "You examine academic requirements, previous degree requirements, "
            "CGPA requirements, prerequisites, English language requirements, "
            "and other important admission conditions."
        ),

        llm=llm,

        verbose=True,
        allow_delegation=False
    )
