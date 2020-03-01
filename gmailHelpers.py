import base64
import email
from apiclient import errors

def GetMessage(service, user_id, msg_id):

    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        
        return message
    except errors.HttpError, error:
        print("An error occurred:", error)

def getLatestSchedule(service, user_id):
    message_id = '<CA+HXoDg1zx4Ua9RnFzN2vg+=YjShJJiQdvqPrZ4H2D-C8-PDwQ@mail.gmail.com>'
    user_list =[]
    try:
        response = service.users().messages().list(userId=user_id).execute()
        print('Received some sort of response')
        if 'messages' in response:
            user_list.extend(response['messages'])
    except errors.HttpError, error:
        print('An error occurred:', error)
    for mail in user_list:
        ebody = service.users().messages().get(userId=user_id, id=mail['id']).execute()
        if 'payload' in ebody and 'headers' in ebody['payload']: #and 'Subject' in ebody['payload']['headers']:
            subject = "It didn't find a subject in this email"
            for header in ebody['payload']['headers']:
                if header['name'] == "Subject":
                    subject = header['value']
            if 'schedule' in subject.lower():
                message_id = mail['id']
                break 
    message = GetMessage(service, user_id, message_id) 
    print(message['payload']['parts'][0]['body'])
    file_data = base64.urlsafe_b64decode(message['payload']['parts'][0]['body']['data'].encode('UTF-8'))
    startInd = file_data.find("<https://docs.google.com/spreadsheets")
    endInd = file_data.find(">", startInd)
    output = file_data[startInd:endInd + 1]
    print(output)
    return output


#service = sheets.googleapis.com

#def getEntriesInSS(service, url):

