import json
c = json.load(open('D:/hermes/whatsapp/session/creds.json'))
print('registered:', c.get('registered'))
print('serverToken exists:', bool(c.get('serverToken')))
print('seq:', c.get('seq'))
print('file keys:', sorted(c.keys()))
print('me exists:', bool(c.get('me')))
if c.get('me'):
    print('me.id:', c['me'].get('id'))
    print('me.lid:', c['me'].get('lid'))
