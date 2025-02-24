import json
import requests

# 百度API
class BaiduAIStreamingClient:
    def __init__(self):
        self.api_key = "ush8XEgzFzNq4EFu4tUSL72l"
        self.secret_key = "kCD2ZNRVNF71BoRWfOKfHmfBdC4wGjYv"
        self.access_token = None
        self.token_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.chat_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
        self.stream = True

    def get_access_token(self):
        """  
        获取access_token  
        """
        url = f"{self.token_url}?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        response = requests.post(url)
        self.access_token = response.json().get("access_token")
        return self.access_token

    async def send_message(self, message):
        """  
        发送消息并获取回复  
        """
        if not self.access_token:
            self.get_access_token()

        url = f"{self.chat_url}?access_token={self.access_token}"
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": self.stream,
            "max_output_tokens": 2048,
            "temperature": 0.2,
            "stop": ["Observation"]

        })
        headers = {
            'Content-Type': 'application/json'
        }
        if self.stream:
            response = requests.post(
                url, headers=headers, data=payload, stream=True)
            for line in response.iter_lines(decode_unicode="utf-8"):

                if line:
                    json_str = line[6:]
                    data = json.loads(json_str)["result"]
                    yield data
        else:
            response = requests.post(
                url, headers=headers, data=payload, stream=False)
            json_str = response.text
            data = json.loads(json_str)["result"]
            yield data

# 使用示例  
# async def main():  
#    api_key = "ush8XEgzFzNq4EFu4tUSL72l"  
#    secret_key = "kCD2ZNRVNF71BoRWfOKfHmfBdC4wGjYv"  
#    client = BaiduAIStreamingClient(api_key, secret_key,stream=True)  
#    async for result in  client.send_message("写一篇20字的春游作文") :  
#       print(result)  


# asyncio.run(main())