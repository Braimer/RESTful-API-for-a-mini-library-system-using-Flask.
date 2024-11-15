from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource


#initializing the flask app
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db'#sqlite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize extensions
db=SQLAlchemy(app)
api=Api(app)

#defines book model,creates book storage in database
class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    author=db.Column(db.String(100),nullable=False)
    year=db.Column(db.Integer,nullable=False)
#create databse tables
with app.app_context():
    db.create_all()
#book resource for crud operations,basic crud endpoints
class BookResource(Resource):
    def get(self):
        #fetch all books
        books=Book.query.all()
        return[{'id':book.id,'title':book.title,'auther':book.author,'year':book.year}for book in books],200
    def post(self):
        from flask import request
        #parse request json
        data=request.get_json()
        new_book=Book(title=data['title'],author=data['author'],year=data['year'])
        db.session.add(new_book)
        db.session.commit()
        return{"message":"Book adde successfully","book_id":new_book.id},201
#add the resource to the api
api.add_resource(BookResource,'/books')


#add individual book endpointa,get,put,delete
class BookDetailResource(Resource):
    def get(self,book_id):
        book=Book.query.get_or_404(book_id)
        return{'id':book.id,'title':book.title,'author':book.author,'year':book.year},200
    def put(self,book_id):
        from flask import request
        book=Book.query.get_or_404(book_id)
        data=request.get_json()
        book.title=data.get('title',book.title)
        book.author=data.get('author',book.author)
        book.year=data.get('year',book.year)
        db.session.commit()
        return{'message':'Book updated successfully'},200
    def delete(self,book_id):
        book=Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return{'message':'book deleted successfully'},200
#add the resource to the api
api.add_resource(BookDetailResource,'/books/<int:book_id>')



if __name__ == '__main__':
    app.run(debug=True)
