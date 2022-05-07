from flask_login import current_user, login_required

from app import db
from app.journal import journal
from flask import render_template, redirect, url_for, request, current_app, jsonify, flash

from app.models import Journal
from app.public_tools import get_epidemic_mode_status


@journal.route("/journal-management")
@login_required
def journal_management():
    """
    The function for rendering the page of journal management
    :return:
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    # query all journals from db
    journal_lst = Journal.query.order_by(Journal.timestamp.desc())

    return render_template("staff/page-list-journals.html", epidemic_mode_on=epidemic_mode_on, journal_lst=journal_lst)


@journal.route("/journal-management/upload-journal", methods=['GET', 'POST'])
@login_required
def upload_journal():
    """
    The function for staffs to upload journals
    :return:
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    # 待改
    return render_template("staff/page-list-journals.html", epidemic_mode_on=epidemic_mode_on)


@journal.route("/journal-management/edit-journal", methods=['GET', 'POST'])
@login_required
def edit_journal():
    """
    The function for editing the journals
    :return:
    """
    pass


@journal.route("/api/journal-management/delete-journal", methods=['POST'])
@login_required
def delete_journal():
    """
    (Using Ajax)
    The function for deleting the journal
    """
    if request.method == 'POST':
        # get info form Ajax
        journal_id = request.form.get("journal_id")

        if journal_id is None:
            current_app.logger.error("info not gotten from Ajax")
            return jsonify({'returnValue': 1})

        try:
            journal_id = int(journal_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify({'returnValue': 1})

        # query this journal from db
        this_journal = Journal.query.get(journal_id)

        if this_journal is None:
            current_app.logger.error("No such journal with this id")
            return jsonify({'returnValue': 1})

        # check if this journal belong to current user
        if this_journal.author_id != current_user.id:
            flash("Permission Denied! You can only delete your own journals!")
            current_app.logger.error("Permission Denied! Some one attempts to delete others' journal")
            return jsonify({'returnValue': 2, 'msg': "Permission Denied! You can only delete your own journals!"})

        # delete this journal
        db.session.delete(this_journal)
        db.session.commit()

        flash("Journal Deleted!")
        return jsonify({'returnValue': 0})
    return jsonify({'returnValue': 1})