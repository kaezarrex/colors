import random
import re

from flask import jsonify, request

from colors.utils import random_color
from colors.web import api, app

COLOR_PATTERN = r'[a-fA-F0-9]{6}'
COLOR = re.compile(COLOR_PATTERN)

@app.route('/blocks', methods=('GET', 'POST',))
def blocks():

    if 'GET' == request.method:
        blocks = []
        for block in api.blocks.all():
            blocks.append({
                'id': str(block['_id']),
                'color': block['color']
            })

        return jsonify({
            'success': True,
            'blocks': blocks
        })

    elif 'POST' == request.method:
        result = {
            'success': False,
            'errors': []
        }

        color = request.form.get('color')
        if color is None or 0 == len(color):
            color = random_color()

        match = COLOR.match(color)

        if match is None:
            result['errors'].append('Invalid color: "%s"' % color)
        else:
            _id = api.blocks.create(color)

            result['success'] = True
            result['id'] = str(_id)

        return jsonify(result)
