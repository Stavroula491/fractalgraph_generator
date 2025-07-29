from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/julia", response_class=HTMLResponse)
async def generate_julia(real: float = Form(...), imag: float = Form(...)):
    k = complex(real, imag)
    width, height = 800, 800
    re_start, re_end = -2, 2
    im_start, im_end = -2, 2
    max_iter = 300

    image = np.zeros((height, width))
    for x in range(width):
        for y in range(height):
            z = complex(re_start + (x / width) * (re_end - re_start),
                        im_start + (y / height) * (im_end - im_start))
            iteration = 0
            while abs(z) <= 2 and iteration < max_iter:
                z = z * z + k
                iteration += 1
            image[y, x] = iteration

    fig, ax = plt.subplots(facecolor='#404040')
    ax.set_facecolor('#404040')
    im = ax.imshow(image, cmap="twilight", extent=(re_start, re_end, im_start, im_end))
    plt.colorbar(im, ax=ax)
    ax.set_title(f"Julia Set (k = {k})", color='black')

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    img_html = f'<img id="juliaImage" src="data:image/png;base64,{img_base64}" width="800" height="800"/>'

    return HTMLResponse(content=img_html)
