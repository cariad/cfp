# pyright: reportPrivateUsage=false

from io import StringIO

from pytest import raises

from cfp import StackParameters
from cfp.exceptions import NoResolverError
from cfp.resolver_factories import (
    ParameterStoreResolverFactory,
    StringResolverFactory,
    UsePreviousValueResolverFactory,
)
from cfp.sources import FromParameterStore, UsePreviousValue


def test_api() -> None:
    sp = StackParameters()
    sp.add("foo", "one")
    sp.add("bar", "two")
    assert sp.api_parameters == [
        {
            "ParameterKey": "foo",
            "ParameterValue": "one",
        },
        {
            "ParameterKey": "bar",
            "ParameterValue": "two",
        },
    ]


def test_add__different_resolver() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo", region="eu-west-2"))
    sp.add("bar", FromParameterStore(name="bar", region="us-east-1"))
    assert len(sp._resolvers) == 2


def test_add__first_resolver() -> None:
    sp = StackParameters()
    assert len(sp._resolvers) == 0
    sp.add("foo", FromParameterStore(name="foo"))
    assert len(sp._resolvers) == 1


def test_add__same_resolver() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo"))
    sp.add("bar", FromParameterStore(name="foo"))
    assert len(sp._resolvers) == 1


def test_add__use_previous_value() -> None:
    sp = StackParameters()
    sp.add("foo", UsePreviousValue())
    sp.add("bar", UsePreviousValue())
    assert len(sp._resolvers) == 1


def test_contains() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo"))
    assert "foo" in sp


def test_contains_false() -> None:
    sp = StackParameters()
    assert "foo" not in sp


def test_find_factory__fail() -> None:
    sp = StackParameters(default_resolvers=False)
    source = FromParameterStore(name="foo")
    with raises(NoResolverError) as ex:
        sp._find_factory(source)
    expect = "no resolver for FromParameterStore(name='foo', region=None, session=None)"
    assert str(ex.value) == expect


def test_find_factory__ok() -> None:
    sp = StackParameters()
    source = FromParameterStore(name="foo")
    factory_type = sp._find_factory(source)
    assert factory_type is ParameterStoreResolverFactory


def test_get() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo"))
    sp.add("woo", "war")
    assert sp["foo"] == FromParameterStore(name="foo")
    assert sp["woo"] == "war"


def test_get__not_exists() -> None:
    sp = StackParameters()
    with raises(KeyError) as ex:
        sp["foo"]
    assert str(ex.value) == "'foo'"


def test_get_factory__no_existing() -> None:
    sp = StackParameters()
    factory = sp._get_factory(ParameterStoreResolverFactory)
    assert isinstance(factory, ParameterStoreResolverFactory)


def test_get_factory__with_existing() -> None:
    sp = StackParameters()
    factory_a = sp._get_factory(ParameterStoreResolverFactory)
    factory_b = sp._get_factory(ParameterStoreResolverFactory)
    assert factory_b is factory_a


def test_init() -> None:
    sp = StackParameters()
    assert sp._factories == {
        ParameterStoreResolverFactory: None,
        StringResolverFactory: None,
        UsePreviousValueResolverFactory: None,
    }


def test_len_0() -> None:
    sp = StackParameters()
    assert len(sp) == 0


def test_len_1() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo"))
    assert len(sp) == 1


def test_len_2() -> None:
    sp = StackParameters()
    sp.add("foo", FromParameterStore(name="foo"))
    sp.add("bar", "bar")
    assert len(sp) == 2


def test_register_resolver() -> None:
    sp = StackParameters(default_resolvers=False)
    assert not sp._factories
    sp.register_resolver(ParameterStoreResolverFactory)
    assert sp._factories == {
        ParameterStoreResolverFactory: None,
    }


def test_render() -> None:
    sp = StackParameters()
    sp.add("foo", "one")
    sp.add("bar", UsePreviousValue())

    writer = StringIO()
    sp.render(writer)

    assert (
        writer.getvalue()
        == """foo = one
bar = <previous value>
"""
    )


def test_render__color() -> None:
    sp = StackParameters()
    sp.add("foo", "one")
    sp.add("bar", UsePreviousValue())

    writer = StringIO()
    sp.render(writer, color=True)

    assert (
        writer.getvalue()
        == """\x1b[38;5;12mfoo\x1b[39m = \x1b[38;5;11mone\x1b[39m
\x1b[38;5;12mbar\x1b[39m = \x1b[38;5;11m<previous value>\x1b[39m
"""
    )
