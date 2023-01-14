from app.calculations import add

def test_add():
    print("testing add func")
    sum = add(5,3)
    assert sum == 8

test_add()