'''Module which is basically ORM object used for create and connection to database
In line 38 it is default salt value for encryption and decryption. 
It is recomended to change it.'''
from cryptography.fernet import InvalidToken
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table
from sqlalchemy.orm import declarative_base, Session
from cryptografer import Cryptografer


meta = MetaData()
password_mannager_db = Table(
    'pm_db', meta,
    Column('id', Integer, primary_key=True), 
    Column('url', String),
    Column('login', String),
    Column('password', String)
)

engine = create_engine('sqlite:///pm_db', echo=False, future=True)
meta.create_all(engine)
Base = declarative_base()

class Password_Mannager_Db(Base):
    __tablename__ = 'pm_db'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    login = Column(String)
    password = Column(String)

class DataBase:
    '''Init for DataBasa. All arguments are optional'''
    def __init__(self, urll = None, loginn = None, passwordd = None) -> None:
        self.url = urll
        self.login = loginn
        self.password = passwordd
        self.item = []
        self.salt = 'django!'
    
    def add_item(self, password):
        '''Method adds nem item to password mannager database. Password is encode by Cryptografer app 
        and in this from is stored in database.'''
        coded_password = Cryptografer(password.encode('utf-8'),
        self.salt.encode('utf-8'),
        self.password.encode('utf-8')
        )
        coded_password.kdf()
        self.item = Password_Mannager_Db(url = self.url,
        login = self.login,
        password = coded_password.encrypt()
        )
        if self.url == None or self.login == None or self.password == None:
            print('*'*25,'\n No data added. Please put necessery data to add:\
url adres of host, login and password.\n','*'*25)
        else:
            with Session(engine) as sesion:
                sesion.add_all([self.item])
                sesion.commit()

    @staticmethod
    def get_items_list():
        '''Method used to return all database content as list. Password is coded bytes form.'''
        list = []
        with Session(engine) as session:
            items = session.query(Password_Mannager_Db).all()
            for item in items:
                list.append([item.id, item.url, item.login, item.password])
                
            return list
    
    
    def get_item_by_id(self, id, password):
        '''Method returns url adres, login and decoded password by id.'''
        list = []
        with Session(engine) as session:
            try:
                item = session.query(Password_Mannager_Db).get(id)
                decoded_password = Cryptografer(password.encode('utf-8'), self.salt.encode('utf-8'), item.password)
                decoded_password.kdf()
                list.append([item.url, item.login, decoded_password.decrypt().decode('utf-8')])
                return list
            except AttributeError:
                print(f'******* No data for id number {id} *******')
            except InvalidToken:
                print(f'******* Wrong password or salt *******')
            except TypeError:
                print(f'******* Please put id number password for decode password saved in database *******')
    
    
    def get_item_by_url(self, url, password, salt = 'django!'):
        '''Method returns url adres, login and decoded password by url adres.'''
        list = []
        with Session(engine) as session:
            try:
                items = session.query(Password_Mannager_Db).filter(Password_Mannager_Db.url == url)
                for item in items:
                    decoded_password = Cryptografer(password.encode('utf-8'), self.salt.encode('utf-8'), item.password)
                    decoded_password.kdf()
                    list.append([item.id, item.login, decoded_password.decrypt().decode('utf-8')])

                return list
            except AttributeError:
                print(f'******* No data for this url adres {url} *******')
            except InvalidToken:
                print(f'******* Wrong password or salt *******')
            except TypeError:
                print(f'******* Please put id number password for decode password saved in database*******')

    @staticmethod
    def delete_item(id):
        with Session(engine) as session:
            session.query(Password_Mannager_Db).filter(Password_Mannager_Db.id == id).delete()
            # session.query(Password_Mannager_Db).get(id).delete()
            session.commit()
            print(f'******* All data for id {id} are deleted. *******')
