// when journal delete buttons are clicked
$(".btn-journal-delete").on('click', function (){
    console.log("delete btn clicked: " + $(this).attr("journal-id"));
    if (confirm("Are your sure to delete this journal?") === true){
        // send ajax request to delete this journal
        deleteJournal($(this).attr("journal-id"))
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
            // remove the row from page
            let tableRowId = "#journal-row-" + journalId;
            $(tableRowId).remove();

        }else if (returnValue === 2){  //attempt to delete other's journal
            //notify the user
            window.alert(response['msg']);
        }
    });
}