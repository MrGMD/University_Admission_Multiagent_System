from crewai import Agent


def create_advisor_agent(llm):

    return Agent(
        role="Senior University Admissions Advisor",

        goal=(
            "Combine the work of all previous agents and produce a clear "
            "preliminary university admission assessment."
        ),

        backstory=(
            "You are a senior academic admissions advisor. "
            "You review admission requirements, eligibility analysis, "
            "and program recommendations and turn them into one clear "
            "student-friendly report."
        ),

        llm=llm,

        verbose=True,
        allow_delegation=False
    )
