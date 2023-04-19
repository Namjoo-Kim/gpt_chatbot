import openai
import json
from config import config

openai.api_key = config.plats_api_key

class Driver:
    def __init__(self):        
        self.chatCompletion = openai.ChatCompletion()
        self.completion = openai.Completion()

    def addMessages(self, userMessages, assistantMessages) :
        messages_1=[
        {"role": "system", "content": "당신은 이제부터 목사님입니다. " +
        "당신이 하는 일은 고민을 종교적으로 답변해주는 일입니다. " +
        "당신의 답변은 최대한 성경을 토대로 답변합니다. " +
        "당신의 답변은 항상 긍정적입니다. " +
        "당신은 무조건 목사님과 같은 말투로 말합니다. " +
        "당신의 답변은 무조건 '친애하는 친구여. 질문을 해줘서 감사하다'고 시작합니다." +
        "당신의 답변은 무조건 이 답변이 도움이 되기를 바란다고 마무리합니다."
        },
        {"role": "user", "content": "안녕하세요."},
        {"role": "assistant", "content": "친애하는 친구여, 당신의 질문에 대해 감사드립니다. 저의 답변이 당신에게 도움이 되기를 바랍니다."},
        ]
            
        if (len(userMessages) != 0):
            messages_1.append(
            {"role": "user", "content": userMessages[len(userMessages)-1]}
            )
            

        print(messages_1)
        response_1 = self.chatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages_1,
        )
        answer_1 = str(response_1.choices[0].message.content).replace("\n", "").strip()
        
        ############
        messages_2 =  """당신은 성격책입니다.
        당신이 하는 일은 고민의 답변을 성경 구절로 알려줍니다.
        당신은 성경목록과 장과 절만으로 대답합니다.
        \nHuman: 신은 정말 있나요? \nAI: 시편 14:1 
        \nHuman: 술을 마시지 않아야 하나요? \nAI: 에베소서 5:18
        \nHuman: 목회자가 사회적인 직업을 함께 겸하고 있는것에 대한 신학적 고찰이 필요합니다. \nAI: 고린도전서 9:22
        """

        prompt = "\nHuman: {} \nAI: ".format(userMessages[len(userMessages)-1])
        messages_2 += prompt
        
        response_2 = self.completion.create(
            engine="text-davinci-003",
            prompt=messages_2,
            temperature=0,
            max_tokens=20,
            # top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            best_of=1,
            stop=[" Human:", " AI:"],
        )
        answer_2 = response_2.choices[0].text.strip()
        
        ###############
        messages_3=[
        {"role": "system", "content": "당신은 이제부터 목사님입니다. " +
        "당신이 하는 일은 기도문을 작성해줍니다. " +
        "당신의 답변은 최대한 성경을 토대로 작성합니다. " +
        "당신의 답변은 항상 긍정적입니다. " +
        "당신의 답변은 무조건 '하나님'으로 시작합니다." +
        "당신의 답변은 무조건 '아멘'으로 마무리합니다."
        },
        {"role": "user", "content": "다음의 글을 토대로 기도문을 작성해 주세요. \n {0}".format(answer_1)},
        ]

        response_3 = self.chatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages_3
        )
        answer_3 = str(response_3.choices[0].message.content).replace("\n", "").strip()
        
        return {"assistant": '<생명의 말씀>' + answer_1 + '<성경 해설>' + answer_2 + '<기도문>' + answer_3}