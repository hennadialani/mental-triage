
import os
import asyncio
import aiohttp
from aiohttp import web
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say

account_sid = "ACe4eda02e83606fc6ab686d1f56e6a7cc"#os.getenv("TWILIO_SID")
auth_token = "e19236a74b5b45736cc240bebcc553bc"#os.getenv("TWILIO_AUTHTOKEN")
url = "http://50a312c7.ngrok.io/voice"

client = Client(account_sid, auth_token)

#@app.route("/voice", methods=['GET', 'POST'])
async def voice(req):
    """Respond to incoming phone calls with a 'Hello world' message"""
    print("begin")
    resp = VoiceResponse()

    resp.say("hello world!", voice='alice')

    return web.Response(text=str(resp))

if __name__ == "__main__":
    #app.run(debug=True)
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(voice())
    app = web.Application()
    app.add_routes([web.get('/', voice),
                web.get('/voice', voice)])

    aiohttp.web.run_app(app)






