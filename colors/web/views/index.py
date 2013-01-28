from flask import render_template

from colors.web import app
from colors.web.views.blocks import COLOR_PATTERN

@app.route('/')
def index():
    '''Return the landing page. An upload form.'''

    return render_template('index.html', COLOR_PATTERN=COLOR_PATTERN)
