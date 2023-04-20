from typing import Optional, Annotated, Any
from fastapi import APIRouter, FastAPI, Response, Request, Depends
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

import uvicorn 

from schema.basemodel import tdingModel, davinciModel, gongowlModel
from module import tding, tding_davinci, gongowl
import os

root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount(
            "/app/static",
            StaticFiles(directory=os.path.join(root, 'app/static')),
            name="static",
        )

app.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

initGongowl = gongowl.Driver()
results = {}

class Main2():
    def __init__(self):
        print('init')
        super().__init__()



    @app.get("/")
    async def read_root():
        with open(os.path.join(root, 'app/home/index.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')

    @app.get("/davinciBot") 
    async def davinciBot():
        with open(os.path.join(root, 'app/home/davinci.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')

    @app.get("/gongowl") 
    async def gongowl():
        with open(os.path.join(root, 'app/home/gongowl.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')


    @app.post("/tdingbot") 
    def tdingbot(Tding: tdingModel ):
        userMessages = Tding.userMessages
        assistantMessages = Tding.assistantMessages
        
        initTding = tding.Driver()
        assistantMessages = initTding.addMessages(userMessages, assistantMessages)

        return assistantMessages

    @app.post("/tdingDavinci") 
    def tdingDavinci(Davinci: davinciModel ):
        userMessages = Davinci.userMessages
        question = Davinci.question

        
        initTding = tding_davinci.Driver()
        assistantMessages = initTding.addMessages(userMessages, question)

        return assistantMessages

    @app.post("/gongOwlclassification/{id}") 
    def gongOwlclassification(gongowlModel: gongowlModel, id: str ):
        userMessages = gongowlModel.userMessages

        print(userMessages)
        result = initGongowl.addMessages(userMessages)

        mes1 = "죄송해요. 입시나 진로에 대해 자세하게 물어봐주세요."
        mes2 = "또 다른 질문을 해보시면 어떨까요?"

        if result in ["입시", mes1, mes2]:
            return result
        
        else:
            initGongowl.saveResult(id, result)
            return "streaming"


    @app.post("/stream/{id}") 
    def stream(id: str):
        
        return initGongowl.stream(id)
      

#python -m uvicorn main:app --reload
def main():
    print('==main()==')    
    uvicorn.run(
    app= "main2:app",
    host="0.0.0.0",
    port=1234,
    reload=False,
    # reload_excludes=["app/files/"],
    )

if __name__ == "__main__":
    main()