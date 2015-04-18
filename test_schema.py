import pytest
from pyschema import Schema, String, Float, Int, WorkingDir, List

class MockSchema(Schema):
    mystring = String(default='hallo')
    myfloat = Float(default=1.1)
    myint = Int(default=2)

class SchemaOfSchema(Schema):
    subschema = MockSchema()

class SchemaWithWorkingDir(Schema):
    workingdir = WorkingDir()

class SchemaWithList(Schema):
    listofint = List(Int(), default=[1,2,3])

class SchemaWithListOfSchemas(Schema):
    listofschema = List(MockSchema(), default=[{'mystring': 'schema1'}, {'myint':1}])

@pytest.fixture
def simpleschema():
    return MockSchema()

def test_items(simpleschema):
    d = dict(simpleschema.items())
    for name in ['mystring', 'myfloat', 'myint']:
        assert name in d

@pytest.fixture(params=[{}, {'mystring': 'no!'}, {'myfloat': 100.}], ids=['empty', 'string', 'float'])
def mockschemadata(request):
    return request.param

def test_validate_empty(simpleschema, mockschemadata):
    param = simpleschema.validate(mockschemadata)
    default = {'mystring': 'hallo', 'myfloat': 1.1, 'myint': 2}
    correct = dict(default.items() + mockschemadata.items())
    assert len(param)==3
    for k,v in correct.items():
        assert k in param
        assert v == param[k]

def test_int():
    i = Int(default=10)
    assert i.default() == 10

def test_unicode_string():
    a = String(u'bla')

def test_subschema():
    schema = SchemaOfSchema()
    p1 = schema.validate({'subschema': {}})
    p2 = schema.validate({})
    assert p1 == p2
    assert p1['subschema']['mystring'] == 'hallo'
    assert p2['subschema']['mystring'] == 'hallo'
    assert p1['subschema']['myfloat'] == 1.1
    assert p2['subschema']['myfloat'] == 1.1

def test_listschema():
    schema = SchemaWithList()
    p = schema.validate({})
    assert p['listofint'] == [1,2,3]

def test_listofschemaschema():
    schema = SchemaWithListOfSchemas()
    p1 = schema.validate({})
    assert len(p1['listofschema']) == 2
    assert p1['listofschema'][0]['mystring'] == 'schema1'
    assert p1['listofschema'][1]['mystring'] == 'hallo'

    p2 = schema.validate({'listofschema': [{}, {'myfloat': 100.}, {}]})
    assert len(p2['listofschema'])==3
    assert p2['listofschema'][1]['myfloat']==100.
