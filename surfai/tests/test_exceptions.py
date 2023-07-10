import pickle

import pytest

import surfai

EXCEPTION_TEST_CASES = [
    surfai.InvalidRequestError(
        "message",
        "param",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    surfai.error.AuthenticationError(),
    surfai.error.PermissionError(),
    surfai.error.RateLimitError(),
    surfai.error.ServiceUnavailableError(),
    surfai.error.SignatureVerificationError("message", "sig_header?"),
    surfai.error.APIConnectionError("message!", should_retry=True),
    surfai.error.TryAgain(),
    surfai.error.Timeout(),
    surfai.error.APIError(
        message="message",
        code=400,
        http_body={"test": "test1"},
        http_status="fail",
        json_body={"text": "iono some text"},
        headers={"request-id": "asasd"},
    ),
    surfai.error.OpenAIError(),
]


class TestExceptions:
    @pytest.mark.parametrize("error", EXCEPTION_TEST_CASES)
    def test_exceptions_are_pickleable(self, error) -> None:
        assert error.__repr__() == pickle.loads(pickle.dumps(error)).__repr__()
