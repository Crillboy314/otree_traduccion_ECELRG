from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

author = 'Su nombre va aquí'

doc = """
Una aplicación de cuestionario que lee sus preguntas de una hoja de cálculo 
(consulte quiz.csv en este directorio).
Hay 1 pregunta por página; el número de páginas en el juego
está determinado por el número de preguntas en el CSV. 
Vea el comentario a continuación sobre cómo aleatorizar el orden de las páginas.
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None

    with open('quiz/quiz.csv') as questions_file:
        questions = list(csv.DictReader(questions_file))

    num_rounds = len(questions)


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.questions.copy()
            ## ALTERNATIVE DESIGN:
            ## para aleatorizar el orden de las preguntas, en su lugar podría hacer:

            # import random
            # randomized_questions = random.sample(Constants.questions, len(Constants.questions))
            # self.session.vars['questions'] = randomized_questions

            ## y para aleatorizar de manera diferente para cada participante, podría utilizar
            ## la técnica random.sample, pero asignar a participant.vars 
            ##En lugar de session.vars.

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = int(question_data['id'])
            p.question = question_data['question']
            p.solution = question_data['solution']


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.IntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(widget=widgets.RadioSelect)
    is_correct = models.BooleanField()

    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]

    def check_correct(self):
        self.is_correct = (self.submitted_answer == self.solution)
