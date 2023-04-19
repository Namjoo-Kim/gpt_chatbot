import openai
from config import config

openai.api_key = config.plats_api_key

#history = "당신은 세계 최고의 점성술사입니다. 당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신의 이름은 챗도지입니다. 당신은 사람의 인생을 매우 명확하게 예측하고 운세에 대한 답을 줄 수 있습니다. 운세 관련 지식이 풍부하고 모든 질문에 대해서 명확히 답변해 줄 수 있습니다."



class Driver:
    def __init__(self):        
        self.completion = openai.Completion()
        
    def addMessages(self, userMessages, question) :
        # history =  """당신은 티딩이라는 사이트 서비스의 챗봇입니다. 당신의 이름은 팅봇입니다.
        # 당신이 하는 일은 티딩의 서비스 이용 방법을 알려줍니다.
        # 당신은 대통령이나 국회의원과 같은 정치적인 질문에 대해 답변을 피합니다.
        # 당신은 식사 메뉴나 음식점을 추천해주지 않습니다.
        # 당신은 긍정적인 편이고, 절대 욕설과 반말을 하지 않습니다.
        # 티딩은 인터넷 사이트를 정기적으로 수집하고, 수집한 데이터가 달라지면 서비스 이용자에게 알림을 통해 달라진 내용을 알려줍니다.
        # 티딩의 서비스를 이용하기 위해서는, 서비스 사용자가 회원가입을 하시고 크롬 익스텐션이나, 아이폰 앱스토어나, 구글 플레이 스토어에서 앱을 다운로드 받아 서비스 사용자가 원하는 사이트를 마음껏 수집할 수 있습니다.
        # 서비스 사용자는 사이트 이름, 사이트 주소를 티딩에 등록하면 됩니다.
        # \nHuman: 당신은 티딩이라는 사이트 서비스의 챗봇입니다. \nAI: 안녕하세요! 어떤 것이든 물어보세요, 최선을 다해 답변해 드리겠습니다."""

        history =  """당신의 일은 교육과 관련된 질문을 분류하는 것입니다.
        분류의 결과는 입시, 진로, 기타로 나눕니다.
        입시는 대학교에 관한 질문입니다.
        진로는 장래 등에 대한 질문입니다.
        그 외의 질문은 기타입니다.
        \nHuman: 서울대학교에 대한 정보를 알려줘. \nAI: 입시
        \nHuman: 나는 나중에 어떤 일을 해야 할까? \nAI: 진로
        \nHuman: 나 너무 배고파. \nAI: 기타
        """

        prompt = "\nHuman: {} \nAI: ".format(question)
        userMessages += prompt
        history += userMessages

        response = self.completion.create(
            engine="text-davinci-003",
            prompt=history,
            temperature=0,
            max_tokens=10,
            # top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            best_of=1,
            stop=[" Human:", " AI:"],
        )
        answer = response.choices[0].text.strip()
        return {"answer": answer, "prompt": userMessages + answer}
    
