from typing import Optional, Annotated, Any
from fastapi import APIRouter, FastAPI, Response, Request, Depends
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

import uvicorn 

from schema.basemodel import tdingModel, davinciModel, gongowlModel
from module import tding, tding_davinci, gongowl
import os

root = os.path.dirname(os.path.abspath(__file__))


class Main(FastAPI):
    def __init__(self, **extra: Any):
        super().__init__(**extra)

        # self._app = FastAPI()
        self.initGongowl = gongowl.Driver()
        self.result = {}

        self.mount(
            "/app/static",
            StaticFiles(directory=os.path.join(root, 'app/static')),
            name="static",
        )

        self.add_middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.add_api_route(path='/', endpoint= self.read_root, methods=['GET'])
        self.add_api_route(path='/tdingbot', endpoint= self.tdingbot, methods=['POST'])

        self.add_api_route(path='/davinciBot', endpoint= self.davinciBot, methods=['GET'])
        self.add_api_route(path='/tdingDavinci', endpoint= self.tdingDavinci, methods=['POST'])

        self.add_api_route(path='/gongowl', endpoint= self.gongowl, methods=['GET'])
        self.add_api_route(path='/gongOwlclassification/{id}', endpoint= self.gongOwlclassification, methods=['POST'])
        self.add_api_route(path='/stream/{id}', endpoint= self.stream, methods=['POST'])


    async def read_root(self):
        with open(os.path.join(root, 'app/home/index.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')


    async def davinciBot(self):
        with open(os.path.join(root, 'app/home/davinci.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')


    async def gongowl(self):
        with open(os.path.join(root, 'app/home/gongowl.html')) as fh :
            data = fh.read()

        return Response(content=data, media_type = 'text/html')


    def tdingbot( self, Tding: tdingModel ):
        userMessages = Tding.userMessages
        assistantMessages = Tding.assistantMessages
        
        initTding = tding.Driver()
        assistantMessages = initTding.addMessages(userMessages, assistantMessages)

        return assistantMessages

    def tdingDavinci(self, Davinci: davinciModel ):
        userMessages = Davinci.userMessages
        question = Davinci.question

        
        initTding = tding_davinci.Driver()
        assistantMessages = initTding.addMessages(userMessages, question)

        return assistantMessages

    def gongOwlclassification(self, gongowlModel: gongowlModel ):
        userMessages = gongowlModel.userMessages
        id = gongowlModel.id

        result = self.initGongowl.addMessages(userMessages)

        mes1 = "죄송해요. 입시나 진로에 대해 자세하게 물어봐주세요."
        mes2 = "또 다른 질문을 해보시면 어떨까요?"

        if result in ["입시", mes1, mes2]:
            return result
        
        else:
            self.result[id] = result
            return "streaming"

        # return result


    def stream(self, id: str):
        def gptstream(result):
            for chunk in result:
                chunk_message = chunk['choices'][0]['delta']  # extract the message

                yield ''.join([m.get('content', '') for m in [chunk_message]])     

        try:
            value = next(gptstream(self.result[id]))
            return value
        except:
            return "stopStreaming"
              

#python -m uvicorn main:app --reload
def main():
    app = Main()

    print('==main()==')    
    uvicorn.run(
    app=app, #"main:app",
    host="0.0.0.0",
    port=1234,
    reload=False,
    # reload_excludes=["app/files/"],
    )

if __name__ == "__main__":
    main()