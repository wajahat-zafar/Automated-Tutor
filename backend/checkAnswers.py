import requests
import time


class CheckAnswers:
    def __init__(self, check_list):
        self.check_list = check_list
        self.result = []

    def check_answers(self):

        API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-MiniLM-L6-v2"
        headers = {
            "Authorization": f"Bearer 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"}
        time.sleep(5)

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        for i in self.check_list:
            print(i)
            output = query(
                {
                    "inputs": {
                        "source_sentence": i[0],
                        "sentences": [i[1]],
                    },
                }
            )

            print('\n', output)

            if output[0] >= 0.75:
                self.result.append(1)
            elif output[0] >= 0.5 and output[0] <= 0.75:
                self.result.append(0.5)
            elif output[0] < 0.5:
                self.result.append(0)

        output = sum(self.result)
        return {"output": output}
