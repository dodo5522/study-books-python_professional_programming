#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from datetime import datetime
from flask import Flask, render_template, redirect, request, escape, Markup
import os
import pytz
import shelve


class DatabaseManager(object):
    """ temp
    """

    def __init__(self, data_file="db.bin", data_key="greeting_list"):
        self.data_file_ = data_file
        self.data_key_ = data_key

        if not os.path.isfile(data_file):
            with shelve.open(data_file, flag='c'):
                pass

    def add_data(self, name, comment, at):
        """ Add data to the local storage database.

        args:
            name: str of user name who commented
            comment: str of comment
            at: datetime object when commented
        returns:
            None
        """

        with shelve.open(self.data_file_) as db:
            greeting_list = db[self.data_key_] if self.data_key_ in db else []

            greeting_list.insert(0, {"name": name, "comment": comment, "at": at})

            db[self.data_key_] = greeting_list

    def load_data(self):
        """ Load data from the local storage database.

        args:
            None
        returns:
            list like below.
            [
                { "name": "hoge", "comment": "fuge", "at": datetime(2016, 11, 9) },
                { "name": "hige", "comment": "fige", "at": datetime(2016, 11, 10) },
                ...
            ]
        raises:
            error: database file does not exist.
        """
        with shelve.open(self.data_file_, "r") as db:
            greeting_list = db.get(self.data_key_)

        return greeting_list


app = Flask(__name__)


def localize(date_time, time_zone="Asia/Tokyo"):
    """ Localize the datetime object with your specified timezone.

    args:
        date_time: Aware datetime object.
    returns:
        datetime object with timezone.
    """
    # return date_time.astimezone(pytz.timezone(time_zone))
    try:
        dt = pytz.timezone(time_zone).localize(date_time)
    except ValueError:
        dt = date_time.astimezone(pytz.timezone(time_zone))
    except:
        raise

    return dt


@app.template_filter("filter_replace_datetime_rounded")
def replace_datetime_rounded(utc_datetime):
    return localize(utc_datetime)


@app.template_filter("filter_replace_br")
def replace_br(html):
    return escape(html).replace("\n", Markup("<br>"))


@app.route("/")
def index():
    """ index.html相当の表示 """
    return render_template("index.html", greeting_list=DatabaseManager().load_data())


@app.route("/post", methods=["POST", ])
def post():
    """ post時の処理相当の表示 """
    name = request.form.get("name")
    comment = request.form.get("comment")
    at = datetime.now(pytz.timezone("UTC"))

    dbm = DatabaseManager()
    dbm.add_data(name, comment, at)

    return redirect("/")


if __name__ == "__main__":
    app.run("localhost", 8000, debug=True)
