from typing import Optional

from sqlalchemy.dialects.postgresql import insert

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Theme,
    Question,
    Answer,
    ThemeModel,
    QuestionModel,
    AnswerModel,
)
from typing import List


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = await ThemeModel.create(title=title)
        return Theme(id=theme.id, title=theme.title)

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        theme = await ThemeModel.query.where(ThemeModel.title == title).gino.first()
        return None if theme is None else Theme(id=theme.id, title=theme.title)

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        theme = await ThemeModel.query.where(ThemeModel.id == id_).gino.first()
        return None if theme is None else Theme(id=theme.id, title=theme.title)

    async def list_themes(self) -> List[Theme]:
        themes = await ThemeModel.query.gino.all()
        return [Theme(id=theme.id, title=theme.title) for theme in themes]

    async def get_answers_of_question(self, question_id: int) -> list[Answer]:
        answers_bd = await AnswerModel.query.where(AnswerModel.question_id == question_id).gino.all()
        return [
            Answer(
                title=ans.title,
                is_correct=ans.is_correct,
            ) for ans in answers_bd
        ]

    async def create_answers(self, question_id, answers: List[Answer]):
        await insert(AnswerModel.__table__) \
            .values(
            [{
                'title': ans.title,
                'is_correct': ans.is_correct,
                'question_id': question_id,
            } for ans in answers]) \
            .on_conflict_do_nothing().gino.scalar()

    async def create_question(
            self, title: str, theme_id: int, answers: List[Answer]
    ) -> Question:

        question_bd = await QuestionModel.create(title=title, theme_id=theme_id)
        question = Question(
            id=question_bd.id,
            title=question_bd.title,
            theme_id=question_bd.theme_id,
            answers=answers
        )

        await self.create_answers(question.id, answers)
        return question

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        question = await QuestionModel.query.where(QuestionModel.title == title).gino.first()
        if question is None:
            return None

        return Question(
            id=question.id,
            title=question.title,
            theme_id=question.theme_id,
            answers=await self.get_answers_of_question(question.id),
        )

    async def list_questions(self, theme_id: Optional[int] = None) -> List[Question]:
        questions = await QuestionModel.query.gino.all()
        return [Question(id=quest.id,
                         title=quest.title,
                         theme_id=quest.theme_id,
                         answers=await self.get_answers_of_question(quest.id))  # TODO need join here
                for quest in questions]
