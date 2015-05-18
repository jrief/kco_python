import unittest
from klarnacheckout.order import Order
from mock import Mock
from hamcrest import ( assert_that, equal_to, greater_than, instance_of,
    is_in, contains)
from tests.matchers import called_once_with, assert_raises


class TestOrder(unittest.TestCase):

    def setUp(self):
        self._connector = Mock()
        self._order = Order(self._connector)

    def test_contenttype(self):
        Order.content_type = "application/json"
        assert_that(
            self._order.get_content_type(),
            equal_to("application/json"))

    def test_getlocation_empty(self):
        assert_that(self._order.location, equal_to(None))

    def test_setLocation(self):
        url = "http://foo"
        self._order.location = url
        assert_that(self._order.location, equal_to(url))

    def test_setlocation_type(self):
        url = 5
        self._order.location = url
        assert_that(self._order.location, instance_of(str))

    def test_parse_marshal_identity(self):
        data = {"foo": "boo"}
        self._order.parse(data)
        assert_that(self._order.marshal(), equal_to(data))

    def test_marshal_has_correct_keys(self):
        key1 = "testKey1"
        value1 = "testValue1"

        key2 = "testKey2"
        value2 = "testValue2"
        self._order.parse({key1: value1,
                           key2: value2})
        marshaldata = self._order.marshal()

        assert_that(key1, is_in(marshaldata))
        assert_that(key2, is_in(marshaldata))
        assert_that(
            dict(self._order),
            equal_to({"testKey1": "testValue1", "testKey2": "testValue2"})
        )

        assert_that(value1, marshaldata[key1])
        assert_that(value2, marshaldata[key2])

    def test_set_get_values(self):
        key1 = "testKey1"
        value1 = "testValue1"

        value2 = "testValue2"

        self._order.parse({key1: value1})
        assert_that(self._order[key1], equal_to(value1))

        self._order.parse({key1: value2})
        assert_that(self._order[key1], equal_to(value2))
        assert_that(self._order, contains(key1))

    def test_set_invalid_key(self):
        key = {"1": "2"}
        value = "testValue"

        with assert_raises(TypeError):
            self._order.parse({key: value})

    def test_get_invalid_key(self):
        key = {"1": "2"}

        with assert_raises(TypeError):
            self._order[key]

    def test_get_unavailable_key(self):
        key = "test"

        with assert_raises(KeyError):
            self._order[key]

    def test_create(self):
        location = "http://stub"
        self._order.base_uri = location
        data = {"foo": "boo"}
        self._order.create(data)

        self._connector.apply.assert_called_once_with(
            "POST", self._order, {"url": location, "data": data})

    def test_create_json(self):
        location = "http://stub"
        self._order.base_uri = location
        data = '{"foo": "boo"}'
        self._order.create(data)

        self._connector.apply.assert_called_once_with(
            "POST", self._order, {"url": location, "data": data})

    def test_fetch(self):
        location = "http://stub"
        self._order.location = location
        self._order.fetch()

        self._connector.apply.assert_called_once_with(
            "GET", self._order, {"url": location})

    def test_update(self):
        data = {"foo": "boo"}
        location = "http://klarna.com/foo/bar/13"
        self._order.location = location
        self._order.update(data)

        self._connector.apply.assert_called_once_with(
            "POST", self._order, {"url": location, "data": data})

    def test_create_alternative_entry_point(self):
        data = {"foo": "boo"}
        uri = "http://klarna.com/foo/bar/15"
        Order.base_uri = uri
        order = Order(self._connector)
        order.create(data)

        self._connector.apply.assert_called_once_with(
            "POST", order, {"url": uri, "data": data})
