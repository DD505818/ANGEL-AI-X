import asyncio

from app.models.sentiment import ingest_sentiment


async def sample_source():
    for text in ["profit up", "bear down"]:
        yield text


def test_ingest_sentiment():
    async def run():
        return [s async for s in ingest_sentiment(sample_source())]

    scores = asyncio.run(run())
    assert scores[0] > 0 and scores[1] < 0
