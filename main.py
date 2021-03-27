import operator
from typing import Dict, Union

from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

MAP_OPERATOR = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
}

cors_origins = ['http://127.0.0.1:8000', 'http://localhost:8000']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalcRequestSchema(BaseModel):
    number_1: int = Field(gt=0, description='First number of an algebraic expression')
    number_2: int = Field(ge=0, description='Second number of an algebraic expression')
    operator: str = Field(max_length=1)


class CalcResponseSchema(BaseModel):
    result: int


class CalcErrorResponseSchema(BaseModel):
    result: str


@app.post(
    '/calc',
    response_model=CalcResponseSchema,
)
def calculate(request: CalcRequestSchema) -> Union[CalcResponseSchema, JSONResponse]:
    try:
        result = MAP_OPERATOR[request.operator](request.number_1, request.number_2)
    except ValidationError as error:
        return JSONResponse(status_code=400, content={'result': error.__str__()})
    except KeyError:
        return JSONResponse(status_code=400, content={'result': 'Use the calculation operators: "+", "-", "*", "/", "^"'})
    return CalcResponseSchema(result=result)
