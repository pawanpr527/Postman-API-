# import requests,json

# # API endpoint with symbol
# url = "https://api.marketstack.com/v1/eod"

# # Your API key
# api_key = "afaa301f7b1b2b2d6bd0b9d22a557914"

# # Query parameters
# params = {
#     'access_key': api_key,
#     'symbols': 'AAPL'  # Apple Inc.
# }

# # Make request
# response = requests.get(url, params=params)

# # Check response
# if response.status_code == 200:
#     data = response.json()
#     print(json.dumps(data,indent=4))
# else:
#     print(f"Error {response.status_code}: {response.text}")

import  pandas as pd
from flask import Flask,redirect,render_template,url_for,request
import redis,json
r = redis.Redis(host='localhost',port=6379,db=1,decode_responses=True)
# api_key = "1a730baa84ed7dda61ab0765961deca6"
# url = "https://api.marketstack.com/v1/eod"

# param = {
#     "access_key" : api_key,
#     "symbols" : "AAPL"
# }
# response = requests.get(url,params=param)

# if response.status_code==200:
#     data = response.json()
#     print(data.keys())    #Give all keys

#     df = pd.DataFrame(data['data'])
#     print(df.columns,df.head(),df.shape)

# if 'data' in data and len(data['data'])>0:
#     print((data['data']))

app = Flask(__name__)

@app.route('/add',methods=['POST'])
def students():
   name = request.json.get('name')
   age = request.json.get('age')
   course = request.json.get('course')
   
   if not name or not age or not course:
      return {"error:All fields are required"} ,400
   student = {"name":name,"age":age,"course":course}
   r.rpush("students" ,json.dumps(student))
   return {"message": "Data added successfully"}, 201

@app.route('/view')
def view():
   student = r.lrange("students",0,-1)
   students = [json.loads(s) for s in student]
   return render_template('index.html',students=students)

@app.route('/delete',methods=['DELETE'])
def delete():
   name = request.json.get('name')
   student = r.lrange("students",0,-1)
   deleted = False
   for s in student:
    students = json.loads(s)
    if students["name"] == name:
        r.lrem("students", 0, s)
        deleted = True
   if deleted:
       return {"message": f"All records with name '{name}' deleted successfully"}, 200
   else:
       return {"error": f"No data found for name '{name}'"}, 404

@app.route('/put',methods=['PUT'])
def put():
   name = request.json.get('name')
   age = request.json.get('age')
   course = request.json.get('course')

   student = r.lrange("students",0,-1)
   change = False
   for i,s in enumerate(student):
      student_data = json.loads(s)
      if student_data["name"]==name:
         
         student_data["age"]=age
         student_data["course"]=course

         update_json = json.dumps(student_data)
         r.lset("students",i,update_json)
         change = True
   if change:
      return {"messege" : f"{name}'s record change successfully "},200
   else:
      return {"error" : f"{name} not found"} ,404
      
if __name__ == '__main__':
    app.run(debug=True)