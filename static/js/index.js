;(function($, socketServerPort) {

    $(document).ready(function() {

        var widths = [1, 2, 3, 4, 6, 12],
            zoomLevel = widths.length - 1,
            viewParams = {},
            ws;

        function setViewParams() {
            viewParams.columns = widths[zoomLevel];
            viewParams.blockSpan = 12 / viewParams.columns;
            viewParams.blockDimension = 100 * viewParams.blockSpan - 30;
            viewParams.borderRadius = viewParams.blockSpan * 5;
            viewParams.boxShadowRadius = viewParams.blockSpan * 10;
        }

        function boxShadow(color) {
            return '0 0 ' + viewParams.boxShadowRadius + 'px #' + color;
        }

        function buildBlock(block) {
            return '<div data-block-id="' + block.id + '" ' + 
                        'class="span' + viewParams.blockSpan + ' block" ' + 
                        'style="height:' + viewParams.blockDimension + 'px;' + 
                               'border-radius:' + viewParams.borderRadius + 'px;' + 
                               'background:#' + block.color + ';' + 
                               'box-shadow:' + boxShadow(block.color) + ';">' + 
                    '</div>';
        }

        function getBlocks() {
            $.get('/blocks', function(data) {

                var html = '',
                    i, block;
                if (data.success) {
                    for (i = 0; i < data.blocks.length; i++) {
                        block = data.blocks[i];

                        if (i % viewParams.columns === 0) {
                            html += '<div class="row block-row">';
                        } 
                        html += buildBlock(block);
                        if ((i+1) % viewParams.columns === 0) {
                            html += '</div>';
                        }
                    }

                    if ((i+1) % viewParams.columns !== 0) {
                        html += '</div>';
                    }

                    // Add the blocks to the DOM
                    $('#blocks').html(html);

                } else {
                    console.error(data.errors);
                }
            });
        }

        function addBlock(color) {
            $.post('/blocks', {color: color}, function(data) {
                if (data.success) {
                    console.log('Success creating new block. Id is ' + data.id);
                } else {
                    console.error(data.errors);
                }
            });
        }

        function changeBlockColor(blockId, color) {
            $('div').find('[data-block-id="' + blockId + '"]').css({
                'background': '#'+color,
                'box-shadow': boxShadow(color)
            });
        }

        // The page initialization and event-binding
        setViewParams();

        $('#add-block-button').click(function(e) {
            var $input = $('input[name="color"]'),
                color = $input.val();

            $input.val('');
            addBlock(color);
            return false;
        });

        $('#zoom-out').click(function(e) {
            if (zoomLevel < widths.length - 1) {
                zoomLevel++;
                setViewParams();
                getBlocks();
            }
        });

        $('#zoom-in').click(function(e) {
            if (zoomLevel > 0) {
                zoomLevel--;
                setViewParams();
                getBlocks();
            }
        });

        // Retrieve and display the blocks
        getBlocks();

        // Obtain a connection to the socket server
        ws = new WebSocket('ws://' + window.location.hostname + ':' + socketServerPort);

        ws.onopen = function() {
            console.log('Successfully created WebSocket connection.');
        }

        ws.onmessage = function(message) {
            console.log('Received a socket message');
            console.dir(message);

            // Route the message
            var data = JSON.parse(message.data);
            if ('change-color' === data.type) {
                blockId = data.block_id;
                color = data.color;

                changeBlockColor(blockId, color);

            } else if ('block-created' === data.type) {
                getBlocks();

            } else if ('block-deleted' === data.type) {
                getBlocks();

            } else {
                console.error('Unrecognized message type: "' + data.type + '"');
            }

        }
    });

})(jQuery, SOCKETSERVER_PORT);

