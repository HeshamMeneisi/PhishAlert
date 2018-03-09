from flask import Flask
from flask import request
from extractor import get_flags
import pickle
import numpy as np

pickled_file = 'model.pyo'

app = Flask(__name__)


@app.route('/checkURL', methods=['POST'])
def checkURL():
    url = request.values['url']

    flags = np.array(get_flags(url))

    result = judge.predict(flags.reshape(1, -1))

    response = "OK"
    if result < 0:
        response = "BAD"

    print(url, flags, response)

    return response

if __name__ == "__main__":
    global judge
    judge = pickle.load(open(pickled_file, 'rb'))
    app.run()