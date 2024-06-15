
#! This is just some just to make pytest happy
    
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4