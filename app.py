import streamlit as st
import pandas as pd
import joblib

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="AI College Advisor",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------
# LOAD DATA
# --------------------------------

data = pd.read_csv("college_data.csv")

# --------------------------------
# HEADER
# --------------------------------

st.title("🎓 AI College Advisor")

st.write(
    "Your personal AI-powered college, course and career advisor."
)

st.divider()

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header("👤 Student Profile")

name = st.sidebar.text_input(
    "Student Name",
    placeholder="Enter your name"
)

education = st.sidebar.selectbox(
    "Education Level",
    [
        "10th",
        "12th",
        "Diploma"
    ]
)

percentage = st.sidebar.number_input(
    "Your Percentage",
    min_value=0.0,
    max_value=100.0,
    value=75.0,
    step=0.1
)

entrance_score = st.sidebar.number_input(
    "Entrance Exam Score",
    min_value=0.0,
    max_value=100.0,
    value=70.0,
    step=1.0
)

budget = st.sidebar.number_input(
    "Maximum Annual Fees (₹)",
    min_value=0,
    max_value=1000000,
    value=100000,
    step=5000
)

# --------------------------------
# STREAM
# --------------------------------

st.sidebar.header("📚 Academic Preference")

stream = st.sidebar.selectbox(
    "Preferred Stream",
    sorted(data["stream"].unique())
)

# --------------------------------
# COURSE
# --------------------------------

available_courses = sorted(
    data[
        data["stream"] == stream
    ]["course"].unique()
)

course = st.sidebar.selectbox(
    "Preferred Course",
    available_courses
)

# --------------------------------
# LOCATION
# --------------------------------

location = st.sidebar.selectbox(
    "Preferred Location",
    sorted(data["location"].unique())
)

# --------------------------------
# INTEREST
# --------------------------------

interest = st.sidebar.selectbox(
    "Area of Interest",
    sorted(data["interest"].unique())
)

# --------------------------------
# SCORE FUNCTION
# --------------------------------

def calculate_score(row):

    score = 0

    # Education
    if education == row["education"]:
        score += 10

    # Percentage
    if percentage >= row["min_percentage"]:
        score += 20

    elif percentage >= row["min_percentage"] - 5:
        score += 10

    # Entrance score
    if entrance_score >= row["entrance_score"]:
        score += 15

    elif entrance_score >= row["entrance_score"] - 5:
        score += 8

    # Stream
    if stream == row["stream"]:
        score += 15

    # Course
    if course == row["course"]:
        score += 15

    # Location
    if location == row["location"]:
        score += 10

    # Budget
    if budget >= row["fees"]:
        score += 5

    # Interest
    if interest == row["interest"]:
        score += 10

    return score


# --------------------------------
# RECOMMENDATION BUTTON
# --------------------------------

if st.sidebar.button(
    "🤖 Get AI Recommendations",
    use_container_width=True
):

    if name.strip() == "":
        st.warning("⚠️ Please enter your name.")

    else:

        # Calculate scores
        data["match_score"] = data.apply(
            calculate_score,
            axis=1
        )

        # Sort
        recommendations = data.sort_values(
            "match_score",
            ascending=False
        ).copy()

        # Top 10
        recommendations = recommendations.head(10)

        # --------------------------------
        # WELCOME
        # --------------------------------

        st.success(
            f"Welcome {name}! 👋 "
            "Here are your personalized recommendations."
        )

        # --------------------------------
        # PROFILE
        # --------------------------------

        st.subheader("📋 Your Profile")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Percentage",
            f"{percentage}%"
        )

        c2.metric(
            "Entrance Score",
            entrance_score
        )

        c3.metric(
            "Budget",
            f"₹{budget:,}"
        )

        c4.metric(
            "Stream",
            stream
        )

        st.divider()

        # --------------------------------
        # TOP RECOMMENDATIONS
        # --------------------------------

        st.subheader("🏆 Top College Recommendations")

        for rank, (_, college) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            score = int(college["match_score"])

            if score >= 80:
                status = "🟢 Excellent Match"

            elif score >= 60:
                status = "🟡 Good Match"

            else:
                status = "🟠 Possible Match"

            st.markdown(
                f"## #{rank} 🏫 {college['college']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**Course:** {college['course']}"
                )

                st.write(
                    f"**Stream:** {college['stream']}"
                )

                st.write(
                    f"**Location:** {college['location']}"
                )

            with col2:

                st.write(
                    f"**Fees:** ₹{college['fees']:,}"
                )

                st.write(
                    f"**Minimum Percentage:** "
                    f"{college['min_percentage']}%"
                )

                st.write(
                    f"**Entrance Score:** "
                    f"{college['entrance_score']}"
                )

            with col3:

                st.write(
                    f"**Career:** {college['career']}"
                )

                st.write(
                    f"**Interest:** {college['interest']}"
                )

                st.write(
                    f"**Match Score:** {score}%"
                )

            st.progress(
                min(score, 100) / 100
            )

            st.info(status)

            st.divider()

        # --------------------------------
        # COURSE RECOMMENDATIONS
        # --------------------------------

        st.subheader("🎯 Recommended Courses")

        course_data = (
            data.groupby(
                "course"
            )["match_score"]
            .max()
            .sort_values(
                ascending=False
            )
            .head(5)
        )

        for course_name, score in course_data.items():

            st.write(
                f"**{course_name}** — "
                f"{int(score)}% match"
            )

            st.progress(
                min(int(score), 100) / 100
            )

        # --------------------------------
        # CAREER RECOMMENDATIONS
        # --------------------------------

        st.subheader("💼 Career Suggestions")

        careers = (
            recommendations[
                "career"
            ]
            .drop_duplicates()
            .head(5)
            .tolist()
        )

        for career in careers:
            st.write(f"🚀 {career}")

        # --------------------------------
        # COMPARISON
        # --------------------------------

        st.subheader("📊 College Comparison")

        comparison = recommendations[
            [
                "college",
                "course",
                "location",
                "fees",
                "match_score"
            ]
        ].copy()

        comparison.columns = [
            "College",
            "Course",
            "Location",
            "Fees",
            "Match Score"
        ]

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

# --------------------------------
# HOME SCREEN
# --------------------------------

else:

    st.subheader(
        "✨ Find Your Best College & Career"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🎓 College Finder")

        st.write(
            "Find colleges based on your "
            "marks, course, location and budget."
        )

    with col2:

        st.markdown("### 🎯 Course Advisor")

        st.write(
            "Explore courses from Science, "
            "Commerce, Arts and Diploma streams."
        )

    with col3:

        st.markdown("### 💼 Career Advisor")

        st.write(
            "Discover career options based "
            "on your interests."
        )

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "🎓 AI College Advisor | AIML Project"
)
