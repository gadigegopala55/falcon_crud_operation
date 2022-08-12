import falcon
import json
import sqlite3

app = application = falcon.App()

connection = sqlite3.connect("post.db",check_same_thread=False)
conn = connection.cursor()

# creating a post data
class Createpost():
    def on_get(self, req, resp):
        try:
            conn.execute("CREATE TABLE IF NOT EXISTS post(title VARCHAR(400),description VARCHAR(400))")
            resp.body = "Successfull"
        except Exception as err:
            resp.body = f'{err}'

# getting data from database
class Gettingdata():
    def on_get(self, req, resp):
        try:
            conn.execute("SELECT * FROM post")
            mydata = conn.fetchall()
            print(mydata)
            resp.body = json.dumps(mydata)
        except Exception as error:
            resp.body = f'{error}'

    def on_post(self, req, resp):
        try:
            data = json.loads(req.stream.read())
            title = data["title"]
            description = data["description"]
            conn.execute(f'INSERT INTO post VALUES("{title}","{description}")')
            connection.commit()
            resp.body = "Data entered successfully"
        except Exception as error:
            resp.body = f'{error}'

    def on_put(self, req, resp):
        try:
            data = json.loads(req.stream.read())
            title = data["title"]
            description = data["description"]
            conn.execute(f'SELECT * FROM post WHERE title="{title}"')
            mydata = conn.fetchall()
            length = len(mydata)
            if length == 0:
                resp.body = "enter valid title"
            else:
                conn.execute(f'UPDATE post SET description="{description}" WHERE title="{title}"')
                connection.commit()
                resp.body = "data updated successfully"
        except Exception as error:
            resp.body = f'{error}'
    
    def on_delete(self, req, resp):
        try:
            data = json.loads(req.stream.read())
            title = data["title"]
            conn.execute(f'SELECT * FROM post WHERE title="{title}"')
            mydata = conn.fetchall()
            length = len(mydata)
            if length == 0:
                resp.body = "enter valid title"
            else:
                conn.execute(f'DELETE FROM post WHERE title="{title}"')
                connection.commit()
                resp.body = "data deleted successfully"
        except Exception as error:
            resp.body = f'{error}'

app.add_route('/createpost', Createpost())
app.add_route('/', Gettingdata())
