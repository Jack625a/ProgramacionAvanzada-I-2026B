#FORMA SECUENCIA (ATENCION A CLIENTES POR LLEGADA)
import time
from multiprocessing import Pool

def platos(n):
    time.sleep(0.01)
    return n*n
inicio=time.time()

#USO DE 4 PROCESOS
with Pool(4) as p:
    pedidos=p.map(platos,range(1000))
    print(pedidos)


#simular 1000 pedidos
#for i in range(10000):
 #   pedidos.append(platos(i))
  #  print(pedidos)

fin=time.time()