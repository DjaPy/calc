import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import app, CalcRequestSchema, CalcResponseSchema


client = TestClient(app)


@pytest.mark.parametrize(
    'number_1, number_2, operator, result',
    [
        (1, 1, '+', 2),
        (2, 3, '*', 6),
        (123, 101, '-', 22),
        (5, 2, '^', 25),
    ]
)
def test_calc(number_1, number_2, operator, result):
    response = client.post(
        '/calc',
        CalcRequestSchema(
            number_1=number_1,
            number_2=number_2,
            operator=operator).json(),
    )
    assert response.status_code == 200
    assert response.json() == CalcResponseSchema(result=result).dict()


@pytest.mark.parametrize(
    'number_1, number_2, operator, result',
    [
        (-1, 1, '+', 2),
        (2, -3, '*', 6),
        (10, 101, '-', 22),
        (0, 2, '^', 25),
    ]
)
def test_calc_value_error(number_1, number_2, operator, result):
    with pytest.raises(ValidationError):
        client.post(
            '/calc',
            CalcRequestSchema(
                number_1=number_1,
                number_2=number_2,
                operator=operator).json(),
        )
