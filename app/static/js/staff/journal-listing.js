/* when journal delete buttons are clicked */
$(".btn-journal-delete").on('click', function (){
    if (confirm("Are your sure to delete this journal?") === true){
        // send ajax request to delete this journal
        deleteJournal($(this).attr("journal-id"));
    }
});

/* when edit journal buttons are clicked */
$(".btn-journal-edit").on('click', function (){
    // get current user id and journal author id to compare
    let currentUserId = $(this).attr("current-user-id");
    let authorId = $(this).attr("author-id");
    // user can only edit their own journals
    if(currentUserId === authorId){
        //get href url
        let url = $(this).attr("href-url");
        location.href = url;
    }else{
        //notify user
        window.alert("Permission Denied! You can change only your own journals.");
    }
});


/*
    ------------------------------ Functions using ajax ------------------------------
*/
function deleteJournal(journalId){
    $.post("/api/journal-management/delete-journal", {
        "journal_id": journalId

    }).done(function (response){
        //get response from server
        let returnValue = response['returnValue'];

        if (returnValue === 0) { //success
            // // remove the row from page
            // let tableRowId = "#journal-row-" + journalId;
            // $(tableRowId).remove();

            // we must refresh the page here
            let url = "/journal-management";
            location.href = url;

        }else if (returnValue === 2){  //attempt to delete other's journal
            //notify the user
            window.alert(response['msg']);
        }
        else if (returnValue === 318)
        {
            let targetURL = response['redirectURL'];
            window.location.href = targetURL;
        }
    });
}