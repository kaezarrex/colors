import random
import re

from flask import jsonify, request

from colors.utils import random_color

from colors.web import app, controller

COLOR_PATTERN = r'[a-fA-F0-9]{6}'
COLOR = re.compile(COLOR_PATTERN)

def format_block(block):
    '''Return a block formatted for JSON serialization.

    @param block: dict
        A block from MongoDB.'''

    return {
        'id': str(block['_id']),
        'color': block['color']
    }


@app.route('/blocks', methods=('GET', 'POST',))
@app.route('/blocks/<block_id>', methods=('GET',))
def blocks(block_id=None):

    if 'GET' == request.method:
        blocks = []
        if block_id is not None:
            block = controller.api.blocks.get(ObjectId(block_id))

            if block is None:
                return 'Block does not exists', 404

            blocks.append(format_block(block))

        for block in controller.api.blocks.all():
            blocks.append(format_block(block))

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
            frequency = 30 * random.random()
            _id = controller.create_block(color, frequency=frequency)

            result['success'] = True
            result['id'] = str(_id)

        return jsonify(result)
