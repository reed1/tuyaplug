from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic, Request
from sanic.response import text, json
import os
from plug import get_plug

app = Sanic('TuyaPlug')
app.static('/public', 'public')

@app.get('/')
@app.ext.template('index.html')
async def handler(request: Request):
    return {}

@app.get('/set/<state>')
async def set(request: Request, state: str):
    res = None
    plug = get_plug()
    if state == 'on':
        res = plug.turn_on()
    elif state == 'off':
        res = plug.turn_off()
    return json(res)

def main():
    app.run(
        host=os.environ['WEB_HOST'],
        port=int(os.environ['WEB_PORT']),
        dev=True
    )

if __name__ == '__main__':
    main()