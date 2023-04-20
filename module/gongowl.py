import openai
from config import config

openai.api_key = config.plats_api_key


class Driver:
    def __init__(self):        
        self.ChatCompletion = openai.ChatCompletion()
        self.result = {}

    def addMessages(self, userMessages) :
        
        messages=[
        {"role": "system", "content": """당신은 반드시 '안내', '입시', '진로', '기타'로만 대답합니다.
        당신의 일은 질문을 분류하는 것입니다.
        '안내'는 당신에 대한 질문입니다. 또는, '이 곳은 뭐하는 곳이야' 같은 질문입니다.
        '입시'는 입학 시험(입시), 대학교에 대한 질문입니다.
        '진로'는 공부, 장래, 학업에 대한 질문입니다.
        그 외의 질문은 '기타'입니다.
        """
        },
        {"role": "user", "content": "넌 누구야?"},
        {"role": "assistant", "content": "안내"},
        {"role": "user", "content": "뭐하는 서비스야?"},
        {"role": "assistant", "content": "안내"},
        {"role": "user", "content": "서울대학교에 대한 정보를 알려줘."},
        {"role": "assistant", "content": "입시"},
        {"role": "user", "content": "입시에 대해 알려줘."},
        {"role": "assistant", "content": "입시"},
        {"role": "user", "content": "입시 정보를 알려줘."},
        {"role": "assistant", "content": "입시"},
        {"role": "user", "content": "나는 나중에 어떤 일을 해야 할까?"},
        {"role": "assistant", "content": "진로"},
        {"role": "user", "content": "난 뭘로 먹고 살아야할까?"},
        {"role": "assistant", "content": "진로"},
        {"role": "user", "content": "나 학업에 관해서 상담해줘"},
        {"role": "assistant", "content": "진로"},
        {"role": "user", "content": "나 너무 배고파."},
        {"role": "assistant", "content": "기타"},
        ]

        messages.append(
        {"role": "user", "content": userMessages}
        )
        
        response = self.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages,
            max_tokens=3,
            temperature=0,
        )

        answer = str(response.choices[0].message.content)#.replace("\n", "").strip()
        print(answer)
        if answer not in ["안내", "입시", "진로", "기타"]:
            print("answer", answer)
        
            return "죄송해요. 입시나 진로에 대해 자세하게 물어봐주세요."
        
        if answer == "안내":
            response = self.anne(userMessages)

            return response
                
        if answer == "입시":
            return "입시"

        if answer == "진로":
            response = self.jinro(userMessages)

            return response
        
        return "또 다른 질문을 해보시면 어떨까요?"


    def anne(self, userMessages):
        messages=[
        {"role": "system", "content": """당신의 이름은 공부엉이입니다.
        당신은 이름을 알려주거나, "입시, 진로에 대해 물어보세요."라고 대답하면 됩니다.
        그 외에 일상 답변은 하지 않습니다. 즉, 다른 답변은 필요없습니다.
        """
        }
        ]

        messages.append(
        {"role": "user", "content": userMessages}
        )

        response = self.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=0.2,
            stream=True
        )
        # answer = str(response.choices[0].message.content).strip()
        # return answer

        return response

    
    def jinro(self, userMessages):
        messages=[
        {"role": "system", "content": """당신은 진로 상담가입니다.
        당신은 질문에 대해서 성심성의껏 대답합니다.
        """
        }
        ]

        messages.append(
        {"role": "user", "content": userMessages}
        )

        response = self.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= messages,
            temperature=1,
            stream=True
        )

        # answer = str(response.choices[0].message.content).strip()
        # return answer

        return response
    

    def saveResult(self, id, result):
        print(id, result)
        self.result[id] = result


    def stream(self, id):
        def gptstream(result):
            for chunk in result:
                chunk_message = chunk['choices'][0]['delta']  # extract the message

                yield ''.join([m.get('content', '') for m in [chunk_message]])     

        try:
            value = next(gptstream(self.result[id]))
            return value
        except:
            return "stopStreaming"