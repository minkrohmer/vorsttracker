import requests
import os
import sys

# +
def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--recipients', required=True)
    args = parser.parse_args()
    
    r = requests.get('http://weerlive.nl/api/json-data-10min.php?key=demo&locatie=Amsterdam')
    
    j = r.json()

    sender        = os.environ['FROM']
    sendgrid_pass = os.environ['SENDGRID_PASSWORD']
    sendgrid_user = os.environ['SENDGRID_USERNAME']
    
    min_temp_morgen = int(j['liveweer'][0]['d1tmin'])
    min_temp_overmorgen = int(j['liveweer'][0]['d2tmin'])
       
    text = "Hallo, het gaat morgen of overmorgen vriezen. Zet je plantjes binnen! Gr. Mink"
    
    if (min_temp_morgen < 1 or min_temp_overmorgen < 1): # Het gaat vriezen
        import sendgrid
        sg =sendgrid.SendGridClient(sendgrid_user, sendgrid_pass)
        message = sendgrid.Mail(subject='Het gaat vriezen! Zet je planten binnen.',
                               text=text,
                               from_email = sender)
    else:
        return
    
    for to in args.recipients.split(','):
        message.add_to(to)
    
    status, msg = sg.send(message)
    print(msg)
    if status is not 200:
        sys.exit(1)
        
if __name__ == "__main__":
    main()  
