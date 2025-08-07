import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import os
# initialize firebase real-time database
cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred,{
 'databaseURL':'https://python-db-test-e10d7-default-rtdb.firebaseio.com/'
})

# create data set
# uncommnent follwoing code if you have no data
# ref = db.reference('/')
# ref.set({
# 	'Books': {
# 		'Book 1': {
# 			'name': 'The Mandibles: A Family, 2029–2047',
# 			'author': 'Lionel Shriver',
# 			'publication_date': '12 May 2016'
# 		},
# 		'Book 2': {
# 			'name': 'The Bitcoin Standard',
# 			'author': 'Saifedean Ammous',
# 			'publication_date': '23 March 2018'
# 		},
# 		'Book 3': {
# 			'name': 'Mastering Bitcoin: Programming the Open Blockchain',
# 			'author': 'Andreas M. Antonopoulos',
# 			'publication_date': '12 June 2017'
# 		}
# 	}
# })

booksRef = db.reference('Books')
books = booksRef.get()


###############
def generate_book_no():
    no_of_books = len(booksRef.get())
    new_book_no = no_of_books+1
    new_book_id = f'Book {no_of_books+1}'
    for book in books :
        if(new_book_id in book):
            new_book_no = new_book_no+1
            new_book_id = f'Book {new_book_no+1}'
            continue
        else:
            new_book_id = f'Book {new_book_no}'
            break
    
    return new_book_id
	

############### Add Book
def add_book(name,pub_date,author='unknown'):
    book_id = generate_book_no()
    booksRef.update({
        book_id: {
            'name': name, 
            'author': author,
            'publication_date': pub_date
        }
    })

############### Edit Book
def update_book(name,book_id):
    ref = db.reference('Books')
    book_ref=ref.child(book_id)
    book_ref.update({ 'name': name })

############### Get Book
def get_book(book_no):
    ref = db.reference('Books')
    book = f'Book {book_no}'
    book_ref=ref.child(book)
    return [book,book_ref.get()]

############### display all books
def get_all_books():
    books = booksRef.get()
    for book in books:
        print(book,books[book])

############## get book indexes/id/keys
def get_book_items():
    book_items =""
    count =0
    books = booksRef.get()
    for book in books:

        if(count==3):
            book_items +="\n"
            count=0
       
        book_items += f"{str(book).split(" ")[1]}={books[book]['name']}"
        book_items += "\t"
        count +=1

    return book_items

############### delete book
def delete_book(book_id):
    book_ref = booksRef.child(book_id)
    book_ref.delete()

############### check valid date input
def try_parsing_date(text):
    formats = ['%d-%m-%Y','%d/%m/%Y']
    for fmt in formats:
        try:
            return datetime.strptime(text,fmt) #formatted = date_obj.strftime("%B %d, %Y")
        except ValueError:
            continue
    raise ValueError("No valid date format found.")


################ clear cmdline
def clear_screen():
     os.system('cls' if os.name == 'nt' else 'clear')


################ add book procedure
def add_procedure():
    book_name = input("Enter book title : ")
    book_author = input("Enter book author : ")
    book_date_pub = try_parsing_date(input("Enter Publication date, start with date ('00-01-2000','00/01/2000') :"))
    
    if book_date_pub:
        book_date_pub = book_date_pub.strftime("%d %B %Y")

    add_book(book_name,book_date_pub,book_author)
    clear_screen()
    get_all_books()


################ delete procedue
def delete_procedure():
    clear_screen()
    print(get_book_items())
    book_choice = input("choose a book to delete e.g 1=book 2, type 1 : ")
    if(book_choice.isdigit()):
        book_key = get_book(book_choice)[0]
        value = get_book(book_choice)[1]
        print(book_key,value)

        prompt = input("Are you sure you want to delete book?(i.e y or n)")
        if(prompt.lower()=="y"):
            delete_book(book_key)
            clear_screen()
    else:
        raise ValueError("Option made is not valid")
    


################# update procedure
def update_procedure():
    clear_screen()
    print(get_book_items())
    book_choice = input("choose a book to edit title e.g 1=book 2, type 1, to access book 2 : ")
    if(book_choice.isdigit()):
        book_key = get_book(book_choice)[0]
        value = get_book(book_choice)[1]
        print(book_key,value)

        prompt = input("Are you sure you want to edit book name/title?(i.e y or n)")
        
        if(prompt.lower()=="y"):
            new_book_name =  input("Enter book title : ")
            update_book(new_book_name,book_key)
            clear_screen()
    else:
        raise ValueError("Option made is not valid")

###############

while True:
    try:
        commands = ['a','r','e','q']
        get_all_books()
        crud_operation = input("What would you like to do today? (a-add book, r-remove book, e-edit book,q-quite) : ")
        option = crud_operation.lower()
        if option.isalpha() and len(option)==1 and (option in commands):
            match option:
                case "a":
                    add_procedure()
                case "r":
                    delete_procedure()
                case "e":
                    update_procedure()
                case "q":
                    break
         
    except Exception as e:
        print(f"An error occurred: {e}")
