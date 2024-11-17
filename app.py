import streamlit as st
import json
import glob
import re
from typing import List
class Question:
    def __init__(self, title_quizz, input_question, input_response_possible, input_correct_response):
        self.title_quizz = title_quizz
        self.title_question = None
        self.input_response_possible = input_response_possible
        self.input_question = input_question
        self.input_correct_response = input_correct_response
        self.response_possible = []
        self.correct_responses = []

    # Input pour saisir la question
    def init_question_title(self):
        self.title_question = self.input_question

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
        self.init_question_title()
        self.init_responses_multiple()
        self.init_correct_responses()
    def get_dict_title_question(self):
        return {"title_question":self.title_question}
    def get_dict_responses_multiple(self):
        return {"response_possible":self.response_possible}
    def get_dict_correct_responses(self):
        return {"correct_responses":self.correct_responses}
    def to_dict(self):
        return {"Question":[self.get_dict_title_question(),self.get_dict_responses_multiple(),self.get_dict_correct_responses()]}


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
    def get_dict_questions(self):
        dict_questions_list = []
        for question in self.questions:
            dict_questions_list.append(question.to_dict())
        return {"Questions_Quizz":dict_questions_list}
    def get_dict_title(self):
        return {"Title_Quizz":self.title}
    def get_dict_count_question(self):
        return {"Count_Questions_Quizz":self.count_question}
    def to_dict(self):
        return {"Quizz":[self.get_dict_questions(),self.get_dict_title(), self.get_dict_count_question()]}


def create_quizz():
    if "mon_quizz" not in st.session_state:
        st.session_state.mon_quizz = Quizz()

    # Titre du quiz
    title_quizz = st.session_state.mon_quizz.title
    if title_quizz is None:
        title = st.text_input(label="Titre du quiz", key="title_quizz")
        if st.button("Start Quiz"):
            if title not in ["", None]:
                st.session_state.mon_quizz.init_quizz(title)
                st.rerun()
            else:
                st.write("Veuillez fournir un titre valide pour le quiz.")
    else:
        st.title(f"Quiz: {title_quizz}")  # Titre du quiz
        
        # Formulaire pour ajouter une question

        # Formulaire avec validation après soumission
        with st.form("add_question_form", clear_on_submit=True):
            # Champs du formulaire
            question = st.text_input(label="Question")
            response_possible = st.text_area(label="Réponses possibles (une par ligne)")
            response_correct = st.text_input(label="Indices des réponses correctes (séparés par des virgules)")

            # Validation après soumission
            if st.form_submit_button("Add Question",):
                errors = []

                # Validation des champs
                if not question.strip():
                    errors.append("La question ne peut pas être vide.")
                if not response_possible.strip():
                    errors.append("Les réponses possibles ne peuvent pas être vides.")
                else:
                    responses = response_possible.split('\n')
                    if len(responses) < 2:
                        errors.append("Il doit y avoir au moins deux réponses possibles.")
                if response_correct.strip():
                    try:
                        correct_indices = list(map(int, response_correct.split(',')))
                        if any(index < 0 or index >= len(responses) for index in correct_indices):
                            errors.append("Les indices des réponses correctes doivent être valides.")
                    except ValueError:
                        errors.append("Les indices des réponses correctes doivent être des entiers séparés par des virgules.")
                else:
                    errors.append("Les indices des réponses correctes ne peuvent pas être vides.")

                # Si des erreurs sont présentes, les afficher
                if errors:
                    st.error("\n".join(errors))
                else:
                    # Ajouter la question et afficher un message de succès
                    new_question = Question(title_quizz, question, response_possible, response_correct)
                    new_question.run()  # Initialise la question avec les bonnes données
                    st.session_state.mon_quizz.add_question(new_question)
                    st.success("Question ajoutée avec succès !")
                    st.session_state[f"question_{title_quizz}"] = ""  # Réinitialiser l'entrée
                    st.session_state[f"response_possible_{title_quizz}"] = ""  # Réinitialiser l'entrée
                    st.session_state[f"correct_responses_{title_quizz}"] = ""  # Réinitialiser l'entrée


        # Afficher les questions ajoutées
        if st.session_state.mon_quizz.questions:
            st.subheader("Questions ajoutées :")
            for idx, q in enumerate(st.session_state.mon_quizz.questions, start=1):
                st.write(f"**Question {idx}:** {q.input_question}")
                st.write(f"- Réponses possibles: {q.response_possible}")
                st.write(f"- Réponses correctes: {q.correct_responses}")
        if st.button("Finish"):
            with open(f"Quizz_{st.session_state.mon_quizz.title}.json", "w") as file:
                # json.dump(st.session_state.mon_quizz.__dict__, file)
                json.dump(st.session_state.mon_quizz.to_dict(), file)
 
def search_quizz():
    return glob.glob("Quizz_*.json")
def load_quizz(list_quizz: List[str], index: int):
    with open(list_quizz[index], "r") as file:
        my_quizz = json.load(file)
    return my_quizz


def start_quizz():
    # Chercher les fichiers de quiz
    list_quizz = search_quizz()
    
    if list_quizz:
        # Extraire les noms des quiz et les nettoyer
        quiz_names = [clean_name_quizz(quizz) for quizz in list_quizz]

        if "selected_quizz" not in st.session_state:
            st.session_state.selected_quizz = quiz_names[0]

        # Afficher une sélection dans Streamlit
        selected_quizz = st.selectbox("Sélectionnez un quiz à lancer :", quiz_names, key="selected_quizz")

        # Récupérer l'index du fichier sélectionné
        selected_index = quiz_names.index(selected_quizz)
        
        # Charger le quiz sélectionné
        if st.button("Lancer le quiz"):
            st.session_state.current_quizz = load_quizz(list_quizz, selected_index)
            st.session_state.quiz_started = True

    else:
        st.write("Aucun quiz disponible.")
    
    # Affichage des questions si un quiz a été lancé
    if st.session_state.get("quiz_started", False):
        my_quizz = st.session_state.current_quizz
        st.write(f"**Quiz: {my_quizz['Quizz'][1]['Title_Quizz']}**")  # Affiche le titre
        
        # Parcourir les questions du quiz
        for idx, question_data in enumerate(my_quizz['Quizz'][0]['Questions_Quizz'], start=1):
            question = question_data['Question'][0]['title_question']
            responses = question_data['Question'][1]['response_possible']
            correct_responses = question_data['Question'][2]['correct_responses']
            
            # Afficher la question
            st.subheader(f"Question {idx}")
            st.write(question)
            
            # Afficher les choix de réponses sous forme de boutons radio
            user_response = st.radio("Choisissez une réponse :", responses, key=f"q_{idx}")

            # Afficher si la réponse est correcte ou incorrecte
            if st.button(f"Vérifier la réponse de la question {idx}", key=f"btn_{idx}"):
                if responses.index(user_response) in correct_responses:
                    st.success("Bonne réponse !")
                else:
                    st.error("Mauvaise réponse.")


    
def clean_name_quizz(name_file):
    mon_quizz = name_file
    mon_quizz = mon_quizz.replace('.json', '')
    mon_quizz = mon_quizz.replace('Quizz_', '',1)
    return mon_quizz
def transfom_name_quizz(new_name_quizz):
    pattern = r"(Quizz_)(\d*)(\.json)"
    match = re.search(pattern, new_name_quizz)
    chiffre = match.group(2)
    #start_file_quizz = match(1)
    json_extension = match.group(3)
    st.write(f"{chiffre=}\n{json_extension=}")

if '__main__' == __name__:
    # create_quizz()
    start_quizz()
    # st.write(search_quizz())