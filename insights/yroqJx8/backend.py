@app.route('/first_api_call')
def first_call():
    return json.dumps({"status" : "ok", "data" : [1,2,3]})
