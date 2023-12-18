document.addEventListener("DOMContentLoaded", function () {
    const isUserAuthenticated = JSON.parse(document.getElementById('is_authenticated').textContent);

    $("#blogCommentTextarea").click(function () {
        if (!isUserAuthenticated) {
            $('#blogCommentModal').modal('show');
        }
    });
});