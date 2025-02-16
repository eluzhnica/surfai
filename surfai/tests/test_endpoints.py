import io
import json

import pytest
import requests

import surfai
from surfai import error


# FILE TESTS
def test_file_upload():
    result = surfai.File.create(
        file=io.StringIO(
            json.dumps({"prompt": "test file data", "completion": "tada"})
        ),
        purpose="fine-tune",
    )
    assert result.purpose == "fine-tune"
    assert "id" in result

    result = surfai.File.retrieve(id=result.id)
    assert result.status == "uploaded"


# CHAT COMPLETION TESTS
def test_chat_completions():
    result = surfai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}]
    )
    assert len(result.choices) == 1


def test_chat_completions_multiple():
    result = surfai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello!"}], n=5
    )
    assert len(result.choices) == 5


def test_chat_completions_streaming():
    result = None
    events = surfai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        stream=True,
    )
    for result in events:
        assert len(result.choices) == 1


# COMPLETION TESTS
def test_completions():
    result = surfai.Completion.create(prompt="This was a test", n=5, engine="ada")
    assert len(result.choices) == 5


def test_completions_multiple_prompts():
    result = surfai.Completion.create(
        prompt=["This was a test", "This was another test"], n=5, engine="ada"
    )
    assert len(result.choices) == 10


def test_completions_model():
    result = surfai.Completion.create(prompt="This was a test", n=5, model="ada")
    assert len(result.choices) == 5
    assert result.model.startswith("ada")


def test_timeout_raises_error():
    # A query that should take awhile to return
    with pytest.raises(error.Timeout):
        surfai.Completion.create(
            prompt="test" * 1000,
            n=10,
            model="ada",
            max_tokens=100,
            request_timeout=0.01,
        )


def test_timeout_does_not_error():
    # A query that should be fast
    surfai.Completion.create(
        prompt="test",
        model="ada",
        request_timeout=10,
    )


def test_user_session():
     with requests.Session() as session:
        surfai.requestssession = session

        completion = surfai.Completion.create(
            prompt="hello world",
            model="ada",
        )
        assert completion


def test_user_session_factory():
    def factory():
        session = requests.Session()
        session.mount(
            "https://",
            requests.adapters.HTTPAdapter(max_retries=4),
        )
        return session

    surfai.requestssession = factory

    completion = surfai.Completion.create(
        prompt="hello world",
        model="ada",
    )
    assert completion
