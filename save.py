import streamlit as st

class Question:
    def __init__(self, title_quizz, input_question, input_response_possible, input_correct_response):
        self.title_quizz = title_quizz
        self.title_question = ""
        self.input_response_possible = input_response_possible
        self.input_question = input_question
        self.input_correct_response = input_correct_response
        self.response_possible = []
        self.correct_responses = []


    # Input pour saisir la question
    def init_question_title(self):
        self.question = self.input_question

    # Input pour les réponses possibles
    def init_responses_multiple(self):
        response_possible = self.input_response_possible
        self.response_possible = response_possible.split('\n')

    # Input pour les index des réponses correctes
    def init_correct_responses(self):
        correct_responses = self.input_correct_response
        self.correct_responses = correct_responses.split(',')
        self.correct_responses = list(map(int, filter(lambda index: index.strip() != '', self.correct_responses)))

    def run(self):
        st.title(f"Quiz: {self.title_quizz}")  # Utilisez st.title directement
        self.init_question_title()
        self.init_responses_multiple()
        self.init_correct_responses()


class Quizz:
    def __init__(self):
        self.questions = []
        self.title = None
        self.count_question = 0

    def init_quizz(self, title):
        self.title = title
    
    def add_question(self, new_question):
        self.questions.append(new_question)
        self.count_question += 1

# Initialisation du quiz dans st.session_state
if "mon_quizz" not in st.session_state:
    st.session_state.mon_quizz = Quizz()

title_quizz = st.session_state.mon_quizz.title
# Saisie du titre du quiz
if title_quizz is None:
    title = st.text_input(label="Titre du quiz", key="title_quizz")
    if st.button("Start Quiz"):
        st.session_state.mon_quizz.init_quizz(title)
else:
    st.write(f"Quiz: {title_quizz}")
    
    # Ajout d'une nouvelle question
    if "current_question" not in st.session_state:
        question = st.text_input(label="Question", key=f"question_{title_quizz}")
        response_possible = st.text_area(label="Réponses possibles (une par ligne)", key=f"response_possible_{title_quizz}")
        response_correct = st.text_input(label="Indices des réponses correctes (séparés par des virgules)", key=f"correct_responses_{title_quizz}")
        st.session_state.current_question = Question(title_quizz, question, response_possible,response_correct)

    # Affiche l'interface pour créer la question actuelle
    st.session_state.current_question.run()

    # Bouton pour ajouter la question actuelle au quiz
    if st.button("Add Question"):
        st.session_state.mon_quizz.add_question(st.session_state.current_question)
        question = st.text_input(label="Question", key=f"question_{title_quizz}")
        response_possible = st.text_area(label="Réponses possibles (une par ligne)", key=f"response_possible_{title_quizz}")
        response_correct = st.text_input(label="Indices des réponses correctes (séparés par des virgules)", key=f"correct_responses_{title_quizz}")
        st.session_state.current_question = Question(title_quizz, question, response_possible,response_correct) # Réinitialise la question pour la prochaine entrée

    # Bouton pour terminer le quiz et afficher les questions
    if st.button("Finish"):
        st.write("Questions ajoutées au quiz :")
        for idx, question in enumerate(st.session_state.mon_quizz.questions):
            st.write(f"Question {idx + 1}: {question.title_question}")
            st.write(f"Réponses possibles : {question.response_possible}")
            st.write(f"Indices des réponses correctes : {question.correct_responses}")
