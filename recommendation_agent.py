from crewai import Agent


def create_recommendation_agent(llm):

    return Agent(
        role="Academic Program Recommendation Specialist",

        goal=(
            "Recommend suitable academic programs based on the student's "
            "education, skills, interests, and eligibility."
        ),

        backstory=(
            "You are an academic program advisor. "
            "You match students with programs that fit their previous "
            "education, technical skills, research interests, and career goals."
        ),

        llm=llm,

        verbose=True,
        allow_delegation=False
    )
