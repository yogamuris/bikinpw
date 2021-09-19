from wtforms import Form, StringField, validators
from wtforms.fields.html5 import URLField

class ShortForm(Form):
    long_url = URLField("", [validators.DataRequired(), validators.URL()],render_kw={"placeholder":"Link to shorten", "autofocus":True})
    short_url = StringField("", render_kw={"placeholder":"bikin.pw/"})