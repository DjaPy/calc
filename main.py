import operator

from fastapi import FastAPI
from pydantic import BaseModel, Field


MAP_OPERATOR = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
}


app = FastAPI()


class CalcRequestSchema(BaseModel):
    number_1: int = Field(gt=0, description='First number of an algebraic expression')
    number_2: int = Field(ge=0, description='Second number of an algebraic expression')
    operator: str = Field(max_length=1, )


class CalcResponseSchema(BaseModel):
    result: int = Field(gt=0)


@app.post('/calc', response_model=CalcResponseSchema)
def calculate(request: CalcRequestSchema) -> CalcResponseSchema:
    result = MAP_OPERATOR[request.operator](request.number_1, request.number_2)
    return CalcResponseSchema(result=result)