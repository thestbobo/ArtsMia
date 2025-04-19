from database.DAO import DAO
from model.model import Model

model = Model()
# model.buildGraph()

res = DAO.get_all_objects()

conn = DAO.get_all_connessioni(model._idMap)

print(len(conn))

print(len(res))
