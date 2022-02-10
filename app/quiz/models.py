from dataclasses import dataclass
from typing import Optional

from app.store.database.gino import db


@dataclass
class Theme:
    id: Optional[int]
    title: str


class ThemeModel(db.Model):
    __tablename__ = "themes"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)


class AnswerModel(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    is_correct = db.Column(db.Boolean(), nullable=False)
    question_id = db.Column(db.Integer(), db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list["Answer"]


class QuestionModel(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    theme_id = db.Column(db.Integer(), db.ForeignKey('themes.id', ondelete='CASCADE'), nullable=False)


@dataclass
class Answer:
    title: str
    is_correct: bool
