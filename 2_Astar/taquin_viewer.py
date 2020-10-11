"""
Module for show taquin's state

Author : Droz William
"""

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
    <head>
        <style>
        .square-box {
            weight: 4em;
            height: 4em;
            display: inline;
            background: #4679BD;
            color: white;
            font-size: 3em;
            border-width:2px;
            border-color:white;
            margin: 2px;
        }
        .square-box-white {
            weight: 4em;
            height: 4em;
            display: inline;
            background: white;
            color: white;
            font-size: 3em;
            border-width:2px;
            border-color:white;
            margin: 2px;
        }
        </style>
        <title>Taquin's state viewer</title>
    </head>
    <body>
        <center>
            <h1>Taquin's state viewer</h1>

"""

HTML_END = """  </center>
    </body>
</html>
"""


def square_box(text):
    return """
    <div class='{}'>
        <span>{}</span>
    </div>
    """.format('square-box' if int(text) != 0 else 'square-box-white', text)


class TaquinViewerHTML(object):
    """
    class that show taquin state in HTML
    """

    def __init__(self, filename='latest.html'):
        self.filename = filename
        self.fd = None

    def __enter__(self):
        self.fd = open(self.filename, 'w')
        self.fd.write(HTML_HEADER)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.fd.close()
        self.fd = None

    def add_taquin_state(self, state, title=""):
        self.fd.write("<h2>{}</h2>".format(title))
        for line in state:
            for e in line:
                self.fd.write(square_box(e))
            self.fd.write('<br />')
        self.fd.write("<hr />")
