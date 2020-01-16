from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn, aiohttp, asyncio
from io import BytesIO
import time

from fastai import *
from fastai.vision import *


model_file_url = 'https://www.dropbox.com/s/2ndjs5lx90x0155/export.pkl?raw=1'
model_file_name = 'export'
classes = ['Inside', 'Side', 'Front','Unproper']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, path/f'{model_file_name}.pkl')
    learn = load_learner(path)
    return learn

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    try:
        html = path/'view'/'index.html'
        return HTMLResponse(html.open().read())
    except Exception as e:
        return JSONResponse(str(e))

@app.route('/analyze-pose', methods=['POST'])
async def analyze(request):
    try:
        t = time.time() # get execution time
        data = await request.form()
        img_bytes = await (data['file'].read())
        img = open_image(BytesIO(img_bytes))
        result,_,prob = learn.predict(img)
        dt = time.time() - t
        # prob = [round(i,3) for i in prob.data.numpy()]
        dtexectime = ("%0.03f seconds" % (dt))
        return JSONResponse({'result-pose': str(result.obj),'executiontime': dtexectime, 'probability':  str(prob)})
    except Exception as e:
        return JSONResponse({'error:',str(e)})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app, host='0.0.0.0', port=5001)

