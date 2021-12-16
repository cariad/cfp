from cfp.resolvers import StringResolver


def test_contains() -> None:
    r = StringResolver()
    r.queue("foo", "bar")
    assert "foo" in r


def test_getitem() -> None:
    r = StringResolver()
    r.queue("foo", "bar")
    assert r["foo"] == "bar"


def test_len() -> None:
    r = StringResolver()
    r.queue("foo", "bar")
    assert len(r) == 1
