const showModal = (modalSelector) => {
    $(modalSelector).modal("show");
}

document.addEventListener("DOMContentLoaded", function () {
    if (window.location.href.includes("/blogs/")) {
        const isUserAuthenticated = JSON.parse(
            document.getElementById("is_authenticated").textContent
        );
        $("#blogCommentTextarea").click(function () {
            if (!isUserAuthenticated) {
                showModal("#blogCommentModal");
            }
        });
    }

    $("#blog_add_close_button").click(function () {
        showModal("#blogAddModal");
    });
});
