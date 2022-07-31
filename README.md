Password mannager is window app based on ORM alchemy and sql database. It is stored passwords in data base. Stored passwords are hased wiht SHA256.
For add new passwords and then read them, password for encryption is needed. It is put by user. There is optional salt for password end it has defoult value. It is recomended to change it in alchemy2.py in line 38 self.salt = ''.
Database is create automatically when first run of the app.
