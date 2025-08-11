from app.models.walk_forward import walk_forward_split


def test_walk_forward_split():
    data = list(range(10))
    splits = list(walk_forward_split(data, train_size=4, test_size=2))
    assert len(splits) == 3
    assert splits[0][0] == [0, 1, 2, 3]
    assert splits[0][1] == [4, 5]
