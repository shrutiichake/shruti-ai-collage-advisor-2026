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
    "Find the colleges and courses that best match your profile."
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
    ["10th", "12th", "Diploma"]
)

percentage = st.sidebar.number_input(
    "Percentage",
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
    step=0.1
)

budget = st.sidebar.number_input(
    "Maximum Annual Fees (₹)",
    min_value=0,
    max_value=1000000,
    value=20000,
    step=1000
)

# --------------------------------
# PREFERENCES
# --------------------------------

st.sidebar.header("🎯 Preferences")

course = st.sidebar.selectbox(
    "Preferred Course",
    sorted(data["course"].unique())
)

location = st.sidebar.selectbox(
    "Preferred Location",
    sorted(data["location"].unique())
)

interest = st.sidebar.selectbox(
    "Area of Interest",
    sorted(data["interest"].unique())
)

# --------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------

def calculate_score(row):

    score = 0

    # Academic percentage
    if percentage >= row["min_percentage"]:
        score += 25
    else:
        difference = row["min_percentage"] - percentage

        if difference <= 5:
            score += 15
        elif difference <= 10:
            score += 8

    # Entrance score
    if entrance_score >= row["entrance_score"]:
        score += 20
    else:
        difference = row["entrance_score"] - entrance_score

        if difference <= 5:
            score += 12
        elif difference <= 10:
            score += 5

    # Course
    if course == row["course"]:
        score += 20

    # Location
    if location == row["location"]:
        score += 15

    # Budget
    if budget >= row["fees"]:
        score += 10

    # Interest
    if interest == row["interest"]:
        score += 10

    return score


# --------------------------------
# BUTTON
# --------------------------------

if st.sidebar.button(
    "🤖 Find Best Colleges",
    use_container_width=True
):

    if name.strip() == "":
        st.warning("⚠️ Please enter your name.")

    else:

        # Calculate score
        data["match_score"] = data.apply(
            calculate_score,
            axis=1
        )

        # Only show colleges with reasonable match
        recommendations = data[
            data["match_score"] >= 40
        ].copy()

        # Sort by score
        recommendations = recommendations.sort_values(
            by="match_score",
            ascending=False
        )

        # --------------------------------
        # STUDENT HEADER
        # --------------------------------

        st.success(
            f"Welcome {name}! 🎓 "
            "Here are your personalized recommendations."
        )

        # --------------------------------
        # PROFILE SUMMARY
        # --------------------------------

        st.subheader("📋 Your Profile")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Percentage",
            f"{percentage}%"
        )

        c2.metric(
            "Entrance Score",
            f"{entrance_score}"
        )

        c3.metric(
            "Budget",
            f"₹{budget}"
        )

        c4.metric(
            "Education",
            education
        )

        st.divider()

        # --------------------------------
        # RECOMMENDATIONS
        # --------------------------------

        st.subheader("🏆 Top College Recommendations")

        if len(recommendations) > 0:

            # Top 5
            top_colleges = recommendations.head(5)

            for index, college in top_colleges.iterrows():

                score = int(college["match_score"])

                if score >= 80:
                    level = "🟢 Excellent Match"

                elif score >= 60:
                    level = "🟡 Good Match"

                else:
                    level = "🟠 Possible Match"

                st.markdown(
                    f"## 🏫 {college['college']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Course:** {college['course']}"
                    )

                    st.write(
                        f"**Location:** {college['location']}"
                    )

                with col2:

                    st.write(
                        f"**Fees:** ₹{college['fees']}"
                    )

                    st.write(
                        f"**Minimum Percentage:** "
                        f"{college['min_percentage']}%"
                    )

                with col3:

                    st.write(
                        f"**Career:** {college['career']}"
                    )

                    st.write(
                        f"**Match:** {score}%"
                    )

                st.progress(
                    score / 100
                )

                st.info(level)

                st.divider()

            # --------------------------------
            # COMPARISON TABLE
            # --------------------------------

            st.subheader("📊 College Comparison")

            comparison = top_colleges[
                [
                    "college",
                    "course",
                    "location",
                    "fees",
                    "min_percentage",
                    "match_score"
                ]
            ].copy()

            comparison.columns = [
                "College",
                "Course",
                "Location",
                "Fees",
                "Min Percentage",
                "Match Score"
            ]

            st.dataframe(
                comparison,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No suitable colleges found. "
                "Try changing your preferences."
            )

else:

    # --------------------------------
    # HOME SCREEN
    # --------------------------------

    st.subheader("✨ How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 1️⃣ Enter Profile")
        st.write(
            "Enter your marks, entrance score "
            "and budget."
        )

    with col2:
        st.markdown("### 2️⃣ Select Preferences")
        st.write(
            "Choose your preferred course, "
            "location and interest."
        )

    with col3:
        st.markdown("### 3️⃣ Get Recommendations")
        st.write(
            "Our recommendation system ranks "
            "suitable colleges for you."
        )

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "🎓 AI College Advisor | AIML Project"
)