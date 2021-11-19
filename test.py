import requests

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

myToken = "xoxb-2262625682512-2251596022705-LmSFD8f8dzrNVAsY6h7DrWje"
# xoxb-2262625682512-2251596022705-LmSFD8f8dzrNVAsY6h7DrWje
post_message(myToken,"#stockauto","kimDDong")
