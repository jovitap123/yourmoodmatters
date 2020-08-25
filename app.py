from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
        return render_template('index.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    feeling = request.form['feeling']
    print(feeling)

    # insert model
    #delete lines below after you add your model
    import random
    model_output = random.randint(0, 1)

    output_feeling= "fine"
    if model_output == 1:
        output_feeling = "distressed"

    return render_template('index.html', output=f"It looks like you are /n {output_feeling}.")


if __name__ =="__main__":
    app.run(debug=True)