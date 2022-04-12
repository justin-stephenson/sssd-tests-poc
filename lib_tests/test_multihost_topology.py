import pytest

from lib.multihost import Topology, TopologyDomain


def test_topology__init():
    dom1 = TopologyDomain('test', master=1)
    dom2 = TopologyDomain('test2', master=1)
    obj = Topology(dom1, dom2)

    assert obj.domains == [dom1, dom2]


def test_topology__get():
    dom1 = TopologyDomain('test', master=1)
    dom2 = TopologyDomain('test2', master=1)
    obj = Topology(dom1, dom2)

    assert obj.get('test') == dom1
    assert obj.get('test2') == dom2

    with pytest.raises(KeyError):
        obj.get('unknown')


def test_topology__describe():
    dom1 = TopologyDomain('test', master=1)
    dom2 = TopologyDomain('test2', master=1)
    obj = Topology(dom1, dom2)

    assert obj.describe() == [dom1.describe(), dom2.describe()]


def test_topology__str():
    dom1 = TopologyDomain('test', master=1)
    dom2 = TopologyDomain('test2', master=1)
    obj = Topology(dom1, dom2)

    assert str(obj) == str([dom1.describe(), dom2.describe()])


def test_topology__contains():
    dom1 = TopologyDomain('test', master=1)
    dom2 = TopologyDomain('test2', master=1)
    obj = Topology(dom1, dom2)

    assert 'test' in obj
    assert 'test2' in obj
    assert 'unknown' not in obj


def test_topology__eq():
    dom1_1 = TopologyDomain('test', master=1)
    dom1_2 = TopologyDomain('test2', master=1)
    obj1 = Topology(dom1_1, dom1_2)

    dom2_1 = TopologyDomain('test', master=1)
    dom2_2 = TopologyDomain('test2', master=1)
    obj2 = Topology(dom2_1, dom2_2)

    dom3_1 = TopologyDomain('test', master=1, client=1)
    dom3_2 = TopologyDomain('test2', master=1)
    obj3 = Topology(dom3_1, dom3_2)

    assert obj1 == obj2
    assert not obj1 == obj3
    assert not obj2 == obj3


def test_topology__ne():
    dom1_1 = TopologyDomain('test', master=1)
    dom1_2 = TopologyDomain('test2', master=1)
    obj1 = Topology(dom1_1, dom1_2)

    dom2_1 = TopologyDomain('test', master=1)
    dom2_2 = TopologyDomain('test2', master=1)
    obj2 = Topology(dom2_1, dom2_2)

    dom3_1 = TopologyDomain('test', master=1, client=1)
    dom3_2 = TopologyDomain('test2', master=1)
    obj3 = Topology(dom3_1, dom3_2)

    assert not obj1 != obj2
    assert obj1 != obj3
    assert obj2 != obj3


def test_topology__le():
    dom1_1 = TopologyDomain('test', master=1)
    dom1_2 = TopologyDomain('test2', master=1)
    obj1 = Topology(dom1_1, dom1_2)

    dom2_1 = TopologyDomain('test', master=1)
    dom2_2 = TopologyDomain('test2', master=1)
    obj2 = Topology(dom2_1, dom2_2)

    dom3_1 = TopologyDomain('test', master=1, client=1)
    dom3_2 = TopologyDomain('test2', master=1)
    obj3 = Topology(dom3_1, dom3_2)

    dom4_1 = TopologyDomain('test3', master=1, client=1)
    dom4_2 = TopologyDomain('test2', master=1)
    obj4 = Topology(dom4_1, dom4_2)

    assert obj1 <= obj2
    assert obj2 <= obj1
    assert obj1 <= obj3
    assert obj2 <= obj3
    assert not obj3 <= obj4
    assert not obj3 <= obj1
    assert not obj3 <= obj2


def test_topology__FromMultihostConfig():
    mhc = {'domains': [
        {
            'type': 'test',
            'hosts': [
                {
                    'name': 'ipa',
                    'external_hostname': 'ipa.test',
                    'role': 'master'
                },
                {
                    'name': 'client',
                    'external_hostname': 'client.test',
                    'role': 'client'
                },
            ],
        },
        {
            'type': 'test2',
            'hosts': [
                {
                    'name': 'client',
                    'external_hostname': 'client.test',
                    'role': 'client'
                },
                {
                    'name': 'client2',
                    'external_hostname': 'client2.test',
                    'role': 'client'
                },
            ],
        },
    ]}

    dom1 = TopologyDomain('test', master=1, client=1)
    dom2 = TopologyDomain('test2', client=2)
    obj1 = Topology(dom1, dom2)
    obj2 = Topology.FromMultihostConfig(mhc)

    assert obj1 == obj2
    assert Topology() == Topology.FromMultihostConfig(None)
