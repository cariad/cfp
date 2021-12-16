# pyright: reportPrivateUsage=false

from mock import Mock, patch
from pytest import raises

from cfp.exceptions import ParameterStoreResolutionError
from cfp.resolvers import ParameterStoreResolver
from cfp.sources.parameter_store import FromParameterStore


def test_consider_session__conflict() -> None:
    r = ParameterStoreResolver()
    r._consider_session(Mock())
    with raises(ParameterStoreResolutionError) as ex:
        r._consider_session(Mock())
    assert str(ex.value) == "boto3 session conflict"


def test_consider_session__first_none() -> None:
    r = ParameterStoreResolver()
    r._consider_session(None)
    assert r._session is None


def test_consider_session__first_value() -> None:
    session = Mock()
    r = ParameterStoreResolver()
    r._consider_session(session)
    assert r._session is session


def test_consider_region__conflict() -> None:
    r = ParameterStoreResolver()
    r._consider_region("eu-west-2")
    with raises(ParameterStoreResolutionError) as ex:
        r._consider_region("us-east-1")
    assert str(ex.value) == "eu-west-2 != us-east-1"


def test_consider_region__first_none() -> None:
    r = ParameterStoreResolver()
    r._consider_region(None)
    assert r._region is None


def test_consider_region__first_value() -> None:
    r = ParameterStoreResolver()
    r._consider_region("eu-west-2")
    assert r._region == "eu-west-2"


def test_contains() -> None:
    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore(name="foo"))
    assert "foo" in r


def test_getitem() -> None:
    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore(name="foo"))
    assert r["foo"] == FromParameterStore(name="foo")


def test_get_session__existing() -> None:
    r = ParameterStoreResolver()
    session = Mock()
    r._session = session
    assert r._get_session() == session


def test_get_session__no_region() -> None:
    r = ParameterStoreResolver()
    session = Mock()
    with patch(
        "cfp.resolvers.parameter_store_resolver.Session",
        return_value=session,
    ) as session_init:
        assert r._get_session() == session
        session_init.assert_called_once_with()


def test_get_session__with_region() -> None:
    r = ParameterStoreResolver()
    r._region = "eu-west-2"
    session = Mock()
    with patch(
        "cfp.resolvers.parameter_store_resolver.Session",
        return_value=session,
    ) as session_init:
        assert r._get_session() == session
        session_init.assert_called_once_with(region_name="eu-west-2")


def test_len() -> None:
    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore(name="foo"))
    assert len(r) == 1


def test_queue() -> None:
    r = ParameterStoreResolver()
    r._queue("foo", FromParameterStore(name="/foo/bar"))
    assert r._map == {
        "/foo/bar": "foo",
    }


def test_resolve__invalid() -> None:
    ssm = Mock()
    ssm.get_parameters = Mock(return_value={"InvalidParameters": ["/goo"]})

    session = Mock()
    session.client = Mock(return_value=ssm)

    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore("/foo", session=session))

    with raises(ParameterStoreResolutionError) as ex:
        list(r.resolve())

    assert str(ex.value) == "Systems Manager failed to resolve some parameters: /goo"


def test_resolve__missing() -> None:
    ssm = Mock()
    ssm.get_parameters = Mock(
        return_value={
            "Parameters": [
                {},
                {
                    "Name": "/bar",
                    "Value": "bar-value",
                },
            ]
        }
    )

    session = Mock()
    session.client = Mock(return_value=ssm)

    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore("/foo", session=session))
    r.queue("bar", FromParameterStore("/bar"))
    assert list(r.resolve()) == [
        {
            "ParameterKey": "bar",
            "ParameterValue": "bar-value",
        },
    ]


def test_resolve__ok() -> None:
    get_parameters = Mock(
        return_value={
            "Parameters": [
                {
                    "Name": "/foo",
                    "Value": "foo-value",
                },
                {
                    "Name": "/bar",
                    "Value": "bar-value",
                },
            ]
        }
    )

    ssm = Mock()
    ssm.get_parameters = get_parameters

    client = Mock(return_value=ssm)
    session = Mock()
    session.client = client

    r = ParameterStoreResolver()
    r.queue("foo", FromParameterStore("/foo", session=session))
    r.queue("bar", FromParameterStore("/bar"))
    assert list(r.resolve()) == [
        {
            "ParameterKey": "foo",
            "ParameterValue": "foo-value",
        },
        {
            "ParameterKey": "bar",
            "ParameterValue": "bar-value",
        },
    ]

    get_parameters.assert_called_once_with(Names=["/foo", "/bar"])
    client.assert_called_once_with("ssm")
