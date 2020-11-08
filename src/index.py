from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    print('args:', request.args)  # display text in console
    print('form:', request.form)
    print('data:', request.data)
    print('json:', request.json)
    print('files:', request.files)
    #print("request:", request)
    

    print(request.args['code'])
    return request.args.get('data', 'none')  # send text to web browser

if __name__ == '__main__':
    app.run(port=80, debug=True)
