from flask_login import current_user

from app.journal import journal
from flask import render_template, redirect, url_for, request, current_app

from app.models import Journal
from app.public_tools import get_epidemic_mode_status


@journal.route("/journal-management")
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


@journal.route("/upload-journal", methods=['GET', 'POST'])
def upload_journal():
    """
    The function for staffs to upload journals
    :return:
    """
    # get whether the epidemic mode is turned on currently
    epidemic_mode_on = get_epidemic_mode_status()

    # 待改
    return render_template("staff/page-list-journals.html", epidemic_mode_on=epidemic_mode_on)