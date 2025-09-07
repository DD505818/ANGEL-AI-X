import pytest

from app.agents.autogpt_optimizer import AutoGPTOptimizer


@pytest.mark.asyncio
async def test_autogpt_suggest(monkeypatch):
    class DummyCompletions:
        async def create(self, model, messages):
            return type(
                "Resp",
                (),
                {"choices": [type("Choice", (), {"message": type("M", (), {"content": "ok"})()})]},
            )()

    class DummyClient:
        def __init__(self, api_key: str):
            self.chat = type("Chat", (), {"completions": DummyCompletions()})()

    monkeypatch.setenv("OPENAI_API_KEY", "x")
    monkeypatch.setattr("app.agents.autogpt_optimizer.AsyncOpenAI", DummyClient)
    opt = AutoGPTOptimizer()
    out = await opt.suggest("hi")
    assert out == "ok"
