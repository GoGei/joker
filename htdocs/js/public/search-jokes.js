$('#searchTextInput').on('keyup', function (e) {
    e.preventDefault();
    let toSearch = $(this).val();
    $('.card-text').each(function () {
        let $currentDiv = $(this).closest('.card');
        if ($(this).text().toLowerCase().indexOf(toSearch.toLowerCase()) != -1) {
            $($currentDiv).show();
        }
        else {
            $($currentDiv).hide();
        }
    });
});