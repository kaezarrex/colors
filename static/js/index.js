;(function($) {

    $(document).ready(function() {

        function getBlocks() {
            $.get('/blocks', function(data) {
                console.log(data);
            });
        }

        function addBlock(color) {
            $.post('/blocks', {color: color}, function(data) {
                if (data.success) {
                    console.log('Success adding block. Id is ' + data.id);
                } else {
                    console.error(data.errors);
                }
            });
        }

        $('#add-block-button').click(function() {
            var color = $('input[name="color"]').val()

            addBlock(color);
        });

        getBlocks();
    });

})(jQuery);
