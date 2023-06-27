import openai, os
import functions_framework

@functions_framework.http
def handleWebhook(request):
    req = request.get_json()
    openai.api_key  = os.environ.get('OPENAI_API_KEY', 'Specified environment variable is not set')

    responseText = ""
    intent = req["queryResult"]["intent"]["displayName"]
    query = req["queryResult"]["queryText"]

    # if intent == "Default Welcome Intent":
    #     responseText = "Hello from a GCF Webhook"
    # elif intent == "get-agent-name":
    #     responseText = "My name is Flowhook"
    # else:
    #     responseText = f"There are no fulfillment responses defined for Intent {intent}"
        
    responseText = get_completion(query)
    print(responseText)

    # You can also use the google.cloud.dialogflowcx_v3.types.WebhookRequest protos instead of manually writing the json object
    res = {"fulfillmentMessages": [{"text": {"text": [responseText]}}]}

    return res



def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt, "name": "Sham"}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        max_tokens=150,
    )
    return response.choices[0].message["content"]