from ml.filter_data import Recommendation

def test(p,f,c):
    return [Recommendation(name="Chicken",protein=2,fat=3,carbs=4) for i in range(4)]
