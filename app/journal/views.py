from datetime import datetime

from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.journal import journal
from flask import render_template, redirect, url_for, request, current_app, jsonify, flash

from app.journal.forms import JournalUploadForm, JournalEditForm
from app.models import Journal
from app.public_tools import get_epidemic_mode_status


@journal.route("/journal-management", methods=['GET', 'POST'])
@login_required
def journal_management():
    """
    The function for rendering the page of journal management
    :return:
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    """ if the search form is submitted """
    if request.method == 'POST':
        key_word = request.form.get("key_word")

        if key_word is None or key_word.strip() == "":
            # query all journals from db
            journal_lst = Journal.query.order_by(Journal.timestamp.desc())
        else:
            # query out journals with this key word in title or body, and sort them by date time
            journal_lst = Journal.query.filter(or_(Journal.title.contains(key_word), Journal.text.contains(key_word))).order_by(Journal.timestamp.desc())

        flash("Your search result is shown below!")

    else:
        # query all journals from db
        journal_lst = Journal.query.order_by(Journal.timestamp.desc())

    return render_template("staff/page-list-journals.html", epidemic_mode_on=epidemic_mode_on, journal_lst=journal_lst)


@journal.route("/journal-management/upload-journal", methods=['GET', 'POST'])
@login_required
def upload_journal():
    """
    The function for staffs to upload journals
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    # upload form
    form = JournalUploadForm()

    # if the form is submitted
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data

        # create a new journal obj
        new_journal = Journal(title=title, text=text, author_id=current_user.id)
        db.session.add(new_journal)
        db.session.commit()

        flash("Journal upload success!")
        # back to journal listing page
        return redirect(url_for("journal.journal_management"))

    return render_template("staff/page-add-journal.html", epidemic_mode_on=epidemic_mode_on, form=form)


@journal.route("/journal-management/edit-journal/<int:journal_id>", methods=['GET', 'POST'])
@login_required
def edit_journal(journal_id):
    """
    The function for editing the journals
    :return:
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    # journal edit form
    form = JournalEditForm()

    # get journal from db
    this_journal = Journal.query.get(journal_id)

    if this_journal is None:
        current_app.logger.error("No such journal with this id")
        return redirect(url_for("journal.journal_management"))

    # check if the user is the author of this journal
    if this_journal.author_id != current_user.id:
        flash("Permission Denied! You can only edit your own journals!")
        current_app.logger.error("Permission Denied! Some one attempts to edit others' journal")
        return redirect(url_for("journal.journal_management"))

    # if the form is submitted
    if form.validate_on_submit():
        # update the last edit time
        this_journal.timestamp = datetime.utcnow()
        # update the journal content
        this_journal.title = form.title.data
        this_journal.text = form.text.data
        # submit to db
        db.session.add(this_journal)
        db.session.commit()

        flash("Journal updated successfully!")
        return redirect(url_for("journal.journal_management"))

    # pre input the current data into this form
    form.title.data = this_journal.title
    form.text.data = this_journal.text

    return render_template("staff/page-modify-journal.html", epidemic_mode_on=epidemic_mode_on, form=form)


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