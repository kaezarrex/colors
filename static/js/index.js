;(function($) {

    $(document).ready(function() {
        
        var NUM_COLUMNS = 12,
            BLOCK_SPAN = 12 / NUM_COLUMNS,
            BLOCK_DIMENSION = 70 * BLOCK_SPAN + 30 * (BLOCK_SPAN - 1);

        function getBlocks() {
            $.get('/blocks', function(data) {

                var html = '',
                    i, block;
                if (data.success) {
                    for (i = 0; i < data.blocks.length; i++) {
                        block = data.blocks[i];

                        if (i % NUM_COLUMNS === 0) {
                            html += '<div class="row block-row">';
                        } 

                        html += '<div class="span' + BLOCK_SPAN + ' block" style="height:' + BLOCK_DIMENSION + 'px;background:#' + block.color + ';"></div>';
                        
                        if ((i+1) % NUM_COLUMNS === 0) {
                            html += '</div>';
                        }
                    }

                    if ((i+1) % NUM_COLUMNS !== 0) {
                        html += '</div>';
                    }

                    $('#blocks').html(html);

                } else {
                    console.error(data.errors);
                }
            });
        }

        function addBlock(color) {
            $.post('/blocks', {color: color}, function(data) {
                if (data.success) {
                    getBlocks();
                } else {
                    console.error(data.errors);
                }
            });
        }

        $('#add-block-button').click(function(e) {
            var color = $('input[name="color"]').val()

            addBlock(color);

            return false;
        });

        getBlocks();
    });

})(jQuery);
