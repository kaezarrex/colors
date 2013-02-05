;(function($, socketServerPort) {

    $(document).ready(function() {

        var viewParams = {},
            blocks = {},
            selectedBlock = null,
            ws;

        function cutHex(h) {return (h.charAt(0)=="#") ? h.substring(1,7):h}
        function hexToR(h) {return parseInt((cutHex(h)).substring(0,2),16)}
        function hexToG(h) {return parseInt((cutHex(h)).substring(2,4),16)}
        function hexToB(h) {return parseInt((cutHex(h)).substring(4,6),16)}
        function decimalToHex(d) { 
            var h = '';
            if (d < 16) {
                h += '0';
            }

            return h + d.toString(16);
        }

        function setViewParams() {
            viewParams.columns = 9;
            viewParams.blockSpan = 1;
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
                               'background:#' + block.color + ';">' + 
                    '</div>';
        }

        function renderBlocks() {
            var i = 0,
                html = '',
                id, block;

            deselectBlock();

            for (id in blocks) {
                if (blocks.hasOwnProperty(id)) {
                    block = blocks[id];

                    if (i % viewParams.columns === 0) {
                        html += '<div class="row block-row">';
                    } 
                    html += buildBlock(block);
                    if ((i+1) % viewParams.columns === 0) {
                        html += '</div>';
                    }
                    i++;
                }
            }

            if ((i+1) % viewParams.columns !== 0) {
                html += '</div>';
            }

            // Add the blocks to the DOM
            $('#blocks').html(html);
        }

        function updateBlockColors(block) {
            block.r = hexToR(block.color);
            block.g = hexToG(block.color);
            block.b = hexToB(block.color);
        }

        function addBlock(block) {
            updateBlockColors(block);
            blocks[block.id] = block;
        }

        function selectBlock(blockId) {
            var block = blocks[blockId];

            deselectBlock();

            $('input[name="frequency"]').removeAttr('disabled');
            $('input[type="range"]').removeAttr('disabled');
            $('#delete-block').removeAttr('disabled');

            selectedBlock = block;

            $('.block[data-block-id="' + blockId + '"]').addClass('selected');
            setFrequency(block);
            setSliders(block);
        }

        function deselectBlock() {
            if (selectedBlock !== null) {
                $('.block[data-block-id="' + selectedBlock.id + '"]').removeClass('selected');
            }
            selectedBlock = null;

            $('input[name="frequency"]').attr('disabled', 'disabled');
            $('input[type="range"]').attr('disabled', 'disabled');
            $('#delete-block').attr('disabled', 'disabled');
        }

        function getBlocks() {
            $.get('/blocks', function(data) {

                var html = '',
                    i, block;
                if (data.success) {
                    blocks = {};
                    for (i = 0; i < data.blocks.length; i++) {
                        addBlock(data.blocks[i]);
                    }
                    renderBlocks();

                } else {
                    console.error(data.errors);
                }
            });
        }

        function getBlock(blockId) {
            $.get('/blocks/' + blockId, function(data) {
                addBlock(data.blocks[0]);
                renderBlocks();
            })

        }

        function postBlock(color) {
            $.post('/blocks', {color: color}, function(data) {
                if (data.success) {
                    console.log('Success creating new block. Id is ' + data.id);
                } else {
                    console.error(data.errors);
                }
            });
        }

        function setFrequency(block) {
            $('input[name="frequency"]').val(block.frequency);
        }

        function setSliders(block) {
            $('input[name="r"]').val(block.r);
            $('input[name="g"]').val(block.g);
            $('input[name="b"]').val(block.b);
        }

        function changeBlockColor(blockId, color) {
            var block = blocks[blockId];

            block.color = color;
            updateBlockColors(blocks[blockId]);

            if (block === selectedBlock) {
                setSliders(block);
            }

            $('div').find('[data-block-id="' + blockId + '"]').css({
                'background': '#'+color
            });
        }

        function changeBlockFrequency(blockId, frequency) {
            var block = blocks[blockId];

            block.frequency = frequency;

            if (block === selectedBlock) {
                setFrequency(block);
            }
        }

        function postBlockFrequency(blockId, frequency) {
            $.post('/blocks/' + blockId + '/frequency', {
                    frequency: frequency
                }, function(data) {
                if (data.success) {
                    console.log('Successfully changed the frequency of block ' + blockId);
                } else {
                    console.error(data.errors);
                }
            });
        }

        function deleteBlock(blockId) {
            delete blocks[blockId];

            if (selectedBlock !== null && selectedBlock.id === blockId) {
                deselectBlock();
            }

            renderBlocks();
        }

        function postDeleteBlock() {
            if (selectedBlock === null) {
                return;
            }

            $.post('/blocks/' + selectedBlock.id + '/delete', function(data) {
                if (data.success) {
                    console.log('Successfully deleted block ' + selectedBlock.id);
                } else {
                    console.error(data.errors);
                }
            });
        }

        // The page initialization and event-binding
        setViewParams();

        $('#add-block-button').click(function(e) {
            var $input = $('input[name="color"]'),
                color = $input.val();

            $input.val('');
            postBlock(color);
            return false;
        });

        $('#blocks').delegate('.block', 'click', function() {
            var blockId = $(this).data('block-id');

            selectBlock(blockId);
        });

        $('input[name="frequency"]').change(function() {
            var blockId = selectedBlock.id,
                frequency = $(this).val();

            postBlockFrequency(blockId, frequency);
        });

        $('#delete-block').click(function() {
            postDeleteBlock();

            return false;
        });

        $('input[type="range"]').change(function() {
            var r,g,b, color;
            if (selectedBlock !== null) {
                r = parseInt($('input[name="r"]').val());
                g = parseInt($('input[name="g"]').val());
                b = parseInt($('input[name="b"]').val());

                color = decimalToHex(r) + decimalToHex(g) + decimalToHex(b);

                $.post('/blocks/' + selectedBlock.id + '/color', 
                    {
                        color: color
                    },
                    function(data) {
                        if (data.success) {
                            console.log('Success changing color');
                        } else {
                            console.error(data.errors);
                        }
                    })
            }
        })

        // Retrieve and display the blocks
        getBlocks();

        // Obtain a connection to the socket server
        ws = new WebSocket('ws://' + window.location.hostname + ':' + socketServerPort);

        ws.onopen = function() {
            console.log('Successfully created WebSocket connection.');
        }

        ws.onmessage = function(message) {
            console.debug('Received a socket message');
            console.dir(message);

            // Route the message
            var data = JSON.parse(message.data);
            if ('change-color' === data.type) {
                blockId = data.block_id;
                color = data.color;

                changeBlockColor(blockId, color);

            } else if ('change-frequency' === data.type) {
                blockId = data.block_id;
                frequency = data.frequency;

                changeBlockFrequency(blockId, frequency);

            } else if ('block-created' === data.type) {
                getBlock(data.block_id);

            } else if ('block-deleted' === data.type) {
                deleteBlock(data.block_id);

            } else {
                console.error('Unrecognized message type: "' + data.type + '"');
            }

        }
    });

})(jQuery, SOCKETSERVER_PORT);

