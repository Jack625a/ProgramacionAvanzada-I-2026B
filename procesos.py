from multiprocessing import Process
import time

def tareaN(n):
    print("Procesando tarea",n)
    time.sleep(2)

inicio=time.time()

procesos=[]
for i in range(5):
    p=Process(target=tareaN,args=(i,))
    procesos.append(p)
    p.start()

for p in procesos:
    p.join()

final=time.time()
print("Tiempo total ",final-inicio)