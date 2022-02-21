from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('exercise8_index.html')


# This page will be the page after the form
@app.route('/report')
def report():
    # Check the user name for the 3 requirements.

    # HINTS:
    # https://stackoverflow.com/questions/22997072/how-to-check-if-lowercase-letters-exist/22997094
    # https://stackoverflow.com/questions/26515422/how-to-check-if-last-character-is-integer-in-raw-input

    # Return the information to the report page html.
    lower_letter = False
    upper_letter = False
    num_end = False

    username = request.args.get('username')
    lower_letter = any(c.islower() for c in username)
    # for letter in username:
    #     if letter.lower() == letter:
    upper_letter = any(c.isupper() for c in username)
    
    num_end = username[-1].isdigit()

    report = lower_letter and upper_letter and num_end
    return render_template('exercise8_report.html', report=report, lower=lower_letter, upper=upper_letter, num_end=num_end)

# @app.route('/thankyou')
# def thankyou():
#     return render_template('exercise8_thankyou.html')

# @app.route('/issues')
# def thankyou():
#     return render_template('exercise8_issues.html') 

if __name__ == '__main__':
    app.run(debug=True)
    