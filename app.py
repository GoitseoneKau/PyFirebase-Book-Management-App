import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred,{
 'databaseURL':'https://books-db-demo-default-rtdb.firebaseio.com/'
})
ref = db.reference('/')
ref.set({
	'Books': {
		'Book 1': {
			'name': 'The Mandibles: A Family, 2029–2047',
			'author': 'Lionel Shriver',
			'publication_date': '12 May 2016'
		},
		'Book 2': {
			'name': 'The Bitcoin Standard',
			'author': 'Saifedean Ammous',
			'publication_date': '23 March 2018'
		},
		'Book 3': {
			'name': 'Mastering Bitcoin: Programming the Open Blockchain',
			'author': 'Andreas M. Antonopoulos',
			'publication_date': '12 June 2017'
		}
	}
})
###############
ref = db.reference('Books')
ref.update({
    'Book 4': {
        'name': 'Why Nations Fail', 
        'author': 'Daron Acemoglu, James A.Robinson',
        'publication_date': '20 March 2012'
    }
})
###############
ref = db.reference('Books')
book_ref = ref.child('Book 2')
book_ref.update({'publication_date':'25 May 2023'})
###############
ref = db.reference('Books')
book_ref=ref.child('Book 1')
book_ref.update({ 'ISBN':'9780007560776'})
###############
ref = db.reference('Books')
book_ref=ref.child('Book 3')
print(book_ref.get())
###############
ref = db.reference('Books')
book_ref = ref.child('Book 2')
book_ref.delete()

