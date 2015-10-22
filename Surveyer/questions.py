import csv
from Surveyer import app


class Question:
    def __init__(self, props):
        qid, kind, args, must_answer = props
        self.qid = qid
        self.kind = kind
        self._args = eval(args)
        for key in self._args:
            setattr(self, key, self._args[key])
        self.must_answer = must_answer
        if self.kind == "s_choice" or self.kind == "m_choice":
            self.choices = [(choice, val) for choice, val in zip(self._choices["values"], self._choices["labels"])]


class SurveyPage:
    def __init__(self, page):
        with app.open_resource('static/questions/page{}.csv'.format(page), mode='r') as f:
            q = [Question(row) for row in csv.reader(f)]
        self.questions = q
