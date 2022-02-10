from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, querystring_schema
from asyncpg import UniqueViolationError, ForeignKeyViolationError

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
    QuestionSchema,
    ThemeIdSchema,
    ListQuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]
        try:
            theme = await self.store.quizzes.create_theme(title=title)
        except UniqueViolationError:
            raise HTTPConflict

        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        theme_id = self.data["theme_id"]

        try:
            question = await self.store.quizzes.create_question(
                    title=title,
                    theme_id=theme_id,
                    answers=[
                        Answer(
                            title=answer["title"],
                            is_correct=answer["is_correct"],
                        ) for answer in self.data['answers']
                    ],
                )
        except UniqueViolationError:
            raise HTTPConflict
        except ForeignKeyViolationError:
            raise HTTPNotFound

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions(
            theme_id=self.data.get("theme_id")
        )
        return json_response(
            data=ListQuestionSchema().dump(
                {
                    "questions": questions,
                }
            )
        )