from model.category import Category
from model.model import Model

myModel = Model()

c = Category(5, "Electric Bikes")
myModel.buildGraph(c)

n, e = myModel.getGraphDetails()
print(f"nodi: {n}, archi: {e}")
