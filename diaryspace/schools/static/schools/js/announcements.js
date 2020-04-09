function deleteAnnouncement(announcementElement) {
    if (!confirm("Вы точно хотите удалить это объявление?"))
        return;
    let $element = $(announcementElement);
    let id = $element.attr("announcement-id");
    $.ajax(
        `/api/announcements/${id}/`,
        {
            method: "DELETE",
            headers: {"X-CSRFToken": Cookies.get("csrftoken")},
            success: () => {
                window.location.reload();
            },
            error: () => {
                alert("Не удалось удалить обьявление.");
            }
        }
    );
}
