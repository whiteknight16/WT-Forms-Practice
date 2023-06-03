from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired,URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    location=StringField('Location URL',validators=[DataRequired(),URL()])
    open_time=StringField('Open Time',validators=[DataRequired()])
    close_time=StringField('Closing Time',validators=[DataRequired()])
    coffee_rating=SelectField("Coffee Rating",choices=[('☕'),('☕☕'),('☕☕☕'),('☕☕☕☕'),('☕☕☕☕☕')],validators=[DataRequired()])
    wifi_rating=SelectField("Wifi Rating",choices=[('✘'),('💪'),('💪💪'),('💪💪💪'),('💪💪💪💪'),('💪💪💪💪💪')],validators=[DataRequired()])
    power_outlet_rating=SelectField("Power Outlet Rating",choices=[('🔌'),('🔌🔌'),('🔌🔌🔌'),('🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌')],validators=[DataRequired()])
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        location_URL=form.location.data
        op_t=form.open_time.data
        cl_t=form.close_time.data
        cr=form.coffee_rating.data
        wr=form.wifi_rating.data
        pr=form.power_outlet_rating.data
        name=form.cafe.data
        data=['\n',name,location_URL,op_t,cl_t,cr,wr,pr]
        filename="./cafe-data.csv"
        with open(filename,mode="a",encoding="utf-8") as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow(data)
        return render_template('add.html')
    
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='',encoding="UTF-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
