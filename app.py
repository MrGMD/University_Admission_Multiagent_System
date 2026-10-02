import streamlit as st

from agents import run_admission_system


# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="University Admission Agent",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------------
# Header
# -----------------------------------

st.title("🎓 University Admission Agent")

st.write(
    "A multi-agent AI system that analyzes admission requirements, "
    "evaluates eligibility, and recommends suitable academic programs."
)


st.divider()


# -----------------------------------
# Student Form
# -----------------------------------

with st.form("admission_form"):

    st.subheader("Student Information")

    name = st.text_input(
        "Student Name"
    )

    previous_degree = st.text_input(
        "Previous / Current Degree",
        placeholder="Example: BS Computer Systems Engineering"
    )

    cgpa = st.text_input(
        "CGPA / GPA",
        placeholder="Example: 3.57 / 4.00"
    )

    desired_degree = st.selectbox(
        "Degree You Want to Apply For",
        [
            "Bachelor's",
            "Master's",
            "PhD"
        ]
    )

    desired_field = st.text_input(
        "Desired Field",
        placeholder="Example: Artificial Intelligence / NLP"
    )

    university = st.text_input(
        "Target University",
        placeholder="Optional"
    )

    skills = st.text_area(
        "Technical / Academic Skills",
        placeholder=(
            "Example: Python, Machine Learning, "
            "Transformers, BERT, NLP"
        )
    )

    experience = st.text_area(
        "Projects / Research / Experience",
        placeholder=(
            "Describe relevant projects, research, "
            "publications, internships, etc."
        )
    )

    english_test = st.text_input(
        "English Language Test",
        placeholder="Example: IELTS 7.0 / TOEFL / Not taken"
    )

    additional_information = st.text_area(
        "Additional Information",
        placeholder="Anything else relevant to your admission"
    )

    submit = st.form_submit_button(
        "🔍 Analyze Admission"
    )


# -----------------------------------
# Run System
# -----------------------------------

if submit:

    if not previous_degree:
        st.warning("Please enter your previous/current degree.")

    elif not desired_field:
        st.warning("Please enter your desired field.")

    else:

        student_data = f"""
        Student Name:
        {name}

        Previous / Current Degree:
        {previous_degree}

        CGPA / GPA:
        {cgpa}

        Desired Degree:
        {desired_degree}

        Desired Field:
        {desired_field}

        Target University:
        {university}

        Technical / Academic Skills:
        {skills}

        Projects / Research / Experience:
        {experience}

        English Language Test:
        {english_test}

        Additional Information:
        {additional_information}
        """

        st.divider()

        st.subheader("🤖 Multi-Agent Analysis")

        with st.spinner(
            "The admission agents are analyzing the student profile..."
        ):

            try:

                result = run_admission_system(
                    student_data
                )

                st.success(
                    "Admission analysis completed!"
                )

                st.divider()

                st.subheader(
                    "🎓 Final Admission Assessment"
                )

                st.markdown(
                    str(result)
                )

            except Exception as error:

                st.error(
                    "The admission system encountered an error."
                )

                st.write(
                    str(error)
                )
            
