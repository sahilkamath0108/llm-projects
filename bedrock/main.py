import boto3
import json

prompt = """
You are a lyrics composer and compose lyrics based on 
a programmer's love for coding.
"""

bedrock = boto3.client(service_name = 'bedrock-runtime')

payload = {
    'prompt' : '[INST]' + prompt + '[/INST]',
    'max_gen_len' : 512,
    'temperature' : 0.5,
    'top_p' : 0.9
}

body = json.dumps(payload)
model_id = "meta.llama2-13b-chat-v1"

resp = bedrock.invoke_model(
    body = body,
    modelId = model_id,
    accept = 'application/json',
    contentType = 'application/json'
)

resp_body = json.loads(resp.get('body').read())
resp_text = resp_body['generation']
print(resp_text)