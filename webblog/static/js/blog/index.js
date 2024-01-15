document.addEventListener("DOMContentLoaded", function () {
    if (window.location.href.includes("/blogs/")) {
        const isUserAuthenticated = JSON.parse(document.getElementById('is_authenticated').textContent);
        $("#blogCommentTextarea").click(function () {
            if (!isUserAuthenticated) {
                $('#blogCommentModal').modal('show');
            }
        });
    }
});
