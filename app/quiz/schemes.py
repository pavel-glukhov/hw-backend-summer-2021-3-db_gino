from marshmallow import Schema, fields, validates, ValidationError


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested("AnswerSchema", many=True, required=True)

    @validates('answers')
    def validate_answers(self, data, **kwargs):
        if len(data) < 2:
            raise ValidationError("There must be at least two possible answers")

        ans_correctness = [ans['is_correct'] for ans in data]

        if ans_correctness.count(True) != 1:
            raise ValidationError("There must be one right answer")


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class ThemeListSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int()


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)