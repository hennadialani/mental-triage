
import os
import asyncio
import aiohttp
import json
import time
from aiohttp import web
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say, Record, Pause

account_sid = "ACe4eda02e83606fc6ab686d1f56e6a7cc"#os.getenv("TWILIO_SID")
auth_token = "e19236a74b5b45736cc240bebcc553bc"#os.getenv("TWILIO_AUTHTOKEN")
url = "http://55ae84ef.ngrok.io/voice"

client = Client(account_sid, auth_token)

'''async def delay(t,func,*args):
    await asyncio.sleep(t)
    func(*args)'''

'''async def voice2(req, resp):
    print("begin")
    resp.say("hello, say stuff", voice='alice')
    #await asyncio.sleep(5)
    resp.record()
    resp.hangup()
    print("end")'''

#@app.route("/voice", methods=['GET', 'POST'])
async def voice(req):
    resp = VoiceResponse()
    #asyncio.ensure_future(voice2(req,resp))
    #ws = web.WebSocketResponse()
    #await ws.prepare(req)

    def voice2():
        resp.say("hello, say stuff", voice='alice')
        
        resp.record(timeout=10)
        time.sleep(5)
        resp.hangup()

    voice2()
    #return ws
    return web.Response(text = str(resp))

if __name__ == "__main__":
    #app.run(debug=True)
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(voice())
    app = web.Application()
    app.router.add_route('GET', '/voice', voice)

    loop = asyncio.get_event_loop()
    f = loop.create_server(app.make_handler(), '0.0.0.0', 8080)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass






