import os
import streamlit as st

from crewai import Agent, Task, Crew, Process, LLM

from requirements_agent import create_requirements_agent
from eligibility_agent import create_eligibility_agent
from recommendation_agent import create_recommendation_agent
from advisor_agent import create_advisor_agent

from programs import get_programs


def get_groq_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to Streamlit Cloud Secrets."
        )

    return LLM(
        model="openai/gpt-oss-120b",
        custom_openai=True,
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key
    )


def run_admission_system(student_data):

    llm = get_groq_llm()

    programs = get_programs()

    # -----------------------------------
    # Create Agents
    # -----------------------------------

    requirements_agent = create_requirements_agent(llm)

    eligibility_agent = create_eligibility_agent(llm)

    recommendation_agent = create_recommendation_agent(llm)

    advisor_agent = create_advisor_agent(llm)

    # -----------------------------------
    # Task 1
    # -----------------------------------

    requirements_task = Task(

        description=f"""
        Analyze the student's information:

        {student_data}

        Available program information:

        {programs}

        Identify the relevant admission requirements for the
        student's requested degree and field.

        Discuss:

        - Previous degree requirement
        - CGPA requirement
        - Relevant academic background
        - Required skills
        - Prerequisites
        - English language requirements
        - Other important conditions

        Only use the supplied program information when making
        program-specific claims.

        Clearly identify information that is not available.
        """,

        expected_output="""
        A clear list of admission requirements relevant to the
        student's requested program.
        """,

        agent=requirements_agent
    )

    # -----------------------------------
    # Task 2
    # -----------------------------------

    eligibility_task = Task(

        description=f"""
        Evaluate the following student's eligibility:

        {student_data}

        Use the admission requirements identified by the previous
        agent.

        Determine:

        1. Requirements the student appears to satisfy
        2. Requirements that may be partially satisfied
        3. Requirements that appear to be missing
        4. Information that needs verification

        Do not invent student information.
        Do not claim official admission.
        """,

        expected_output="""
        A structured eligibility assessment containing:

        - Satisfied requirements
        - Possible gaps
        - Missing information
        - Items requiring verification
        """,

        agent=eligibility_agent,

        context=[requirements_task]
    )

    # -----------------------------------
    # Task 3
    # -----------------------------------

    recommendation_task = Task(

        description=f"""
        Recommend suitable academic programs for this student:

        {student_data}

        Available programs:

        {programs}

        Consider:

        - Previous degree
        - CGPA
        - Technical skills
        - Research interests
        - Desired field
        - Eligibility analysis

        Explain why each recommended program fits the student's
        background.

        Do not claim that the student is officially admitted.
        """,

        expected_output="""
        A list of suitable academic programs with a short
        explanation for each recommendation.
        """,

        agent=recommendation_agent,

        context=[
            requirements_task,
            eligibility_task
        ]
    )

    # -----------------------------------
    # Task 4
    # -----------------------------------

    advisor_task = Task(

        description=f"""
        Prepare the final preliminary admission assessment.

        Student information:

        {student_data}

        Combine the outputs of all previous agents.

        The report must contain:

        ## 1. Student Profile

        Brief summary of the student's academic background.

        ## 2. Admission Requirements

        Important requirements identified by the system.

        ## 3. Eligibility Assessment

        Explain which requirements appear satisfied and
        which may have gaps.

        ## 4. Program Recommendations

        List suitable programs and explain the fit.

        ## 5. Possible Gaps

        Clearly identify missing or uncertain information.

        ## 6. Next Steps

        Give practical steps the student should take.

        Important:

        This is a preliminary AI assessment.
        It is NOT an official university admission decision.

        Do not invent university-specific requirements.
        """,

        expected_output="""
        A complete and well-organized preliminary university
        admission assessment.
        """,

        agent=advisor_agent,

        context=[
            requirements_task,
            eligibility_task,
            recommendation_task
        ]
    )

    # -----------------------------------
    # Create Crew
    # -----------------------------------

    crew = Crew(

        agents=[
            requirements_agent,
            eligibility_agent,
            recommendation_agent,
            advisor_agent
        ],

        tasks=[
            requirements_task,
            eligibility_task,
            recommendation_task,
            advisor_task
        ],

        process=Process.sequential,

        verbose=True
    )

    # -----------------------------------
    # Run Crew
    # -----------------------------------

    result = crew.kickoff()

    return result
