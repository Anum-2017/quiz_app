import streamlit as st
import json
import random

# Load questions from JSON
def load_questions():
    try:
        with open("quiz_questions.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "page" not in st.session_state:
    st.session_state.page = "home"
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = []
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False

# Load quiz data
quiz_data = load_questions()

# Define categories
categories = list(quiz_data.keys())

# Button Styling
button_style = """
    <style>
        div.stButton > button {
            background-color: #28a745;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #218838;
            transform: scale(1.05);
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# Sidebar Instructions
st.sidebar.title("📜 Quiz Instructions")
st.sidebar.markdown("""
1️⃣ Select a category.  
2️⃣ Read the question carefully.  
3️⃣ Choose an answer and submit it.  
4️⃣ Get feedback and explanation.  
5️⃣ Your score is tracked throughout the quiz.  
6️⃣ Last question submission takes you to the score page.  
""")

st.sidebar.markdown("---")
st.sidebar.markdown("📢 **Good Luck!** 🚀")

# Home Page
if st.session_state.page == "home":
    st.markdown("""
        <div style="text-align: center;">
            <h1>🎓 Python Quiz App</h1>
            <p style="font-size: 18px;">Test your Python knowledge across multiple topics! 🚀</p>
        </div>
    """, unsafe_allow_html=True)

   
    st.session_state.player_name = st.text_input("Enter your name:", "")

    if st.button("Start Quiz"):
        if st.session_state.player_name.strip():
            st.session_state.page = "category_selection"
            st.rerun()
        else:
            st.warning("Please enter your name before starting!")

# Category Selection Page
elif st.session_state.page == "category_selection":
    st.header("📚 Select a Quiz Category")

    st.session_state.selected_category = st.selectbox("Choose a category:", ["Select"] + categories, key="category_select")

    if st.session_state.selected_category and st.session_state.selected_category != "Select":
        if st.button("Start Quiz"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            
            # Shuffle questions and options
            questions = quiz_data.get(st.session_state.selected_category, [])
            random.shuffle(questions)
            for q in questions:
                random.shuffle(q["options"])
            
            st.session_state.shuffled_questions = questions
            st.session_state.page = "quiz"
            st.rerun()

# Quiz Page
elif st.session_state.page == "quiz":
    questions = st.session_state.shuffled_questions
    total_questions = len(questions)

    if st.session_state.question_index < total_questions:
        question = questions[st.session_state.question_index]
        st.subheader(f"**Q{st.session_state.question_index + 1}: {question['question']}**")

        options = question["options"]
        selected_answer = st.radio("Select an option:", options, key=f"q{st.session_state.question_index}")

        # Check answer on submission
        if st.button("Submit Answer") and not st.session_state.show_feedback:
            st.session_state.selected_answer = selected_answer
            st.session_state.show_feedback = True

            if selected_answer == question["answer"]:
                st.session_state.score += 1
                st.session_state.feedback_message = "✅ Correct! 🎉 Keep going!"
                st.session_state.feedback_type = "success"
            else:
                st.session_state.feedback_message = f"❌ Incorrect! The correct answer is: {question['answer']}"
                st.session_state.feedback_type = "error"

            st.rerun()

        # Show feedback
        if st.session_state.show_feedback:
            if st.session_state.feedback_type == "success":
                st.success(st.session_state.feedback_message)
            else:
                st.error(st.session_state.feedback_message)

            # Show Explanation
            if "explanation" in question and question["explanation"].strip():
                st.markdown(f"📖 **Explanation:** {question['explanation']}")

            # If last question, go to score page
            if st.session_state.question_index == total_questions - 1:
                if st.button("View Score"):
                    st.session_state.page = "score"
                    st.rerun()
            else:
                if st.button("Next Question"):
                    st.session_state.question_index += 1
                    st.session_state.show_feedback = False
                    st.session_state.selected_answer = None
                    st.rerun()

        # Progress Bar
        progress = (st.session_state.question_index + 1) / total_questions
        st.progress(progress)
        st.write(f"**Progress: {int(progress * 100)}% Completed**")

# Score Page
elif st.session_state.page == "score":
    st.markdown('<h2 style="text-align: center;">🎉 Quiz Completed! 🎉</h2>', unsafe_allow_html=True)

    # Score display with better UI
    st.markdown(f"""
    <div style="border: 2px solid #28a745; padding: 20px; border-radius: 10px; text-align: center; margin-top: 20px;">
        <h2 style="color: #28a745;">🏆 Final Score: {st.session_state.score} / {len(st.session_state.shuffled_questions)}</h2>
        <p style="margin-top: 15px;">Great job, {st.session_state.player_name}! Keep practicing and improving! 🚀</p>
    </div>
    <br><br>
""", unsafe_allow_html=True)

    # Restart button
    if st.button("🔄 Restart Quiz"):
        st.session_state.page = "home"
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.show_feedback = False
        st.rerun()
