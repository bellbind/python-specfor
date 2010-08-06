from specfor import the, spec

count_mock_spec = spec.of("mock with count call")
@count_mock_spec.that("count just")
def behavior(its):
    from specfor import mock
    
    pass

# TODO: spec for just, until, over, between

spec.publish(globals())
