from werkzeug.wrappers import Request, Response, ResponseStream
# import something form base and other modules
from app import db
from app.base_class import Base
from app.client_credit.models import ClientCredit
from app.mod_auth.models import User


class middleware():
    # middleware base 

    # init
    def __init__(self, app):
        self.app = app
    
    # save user data to database
    def save_db(self):
        db.session.add(self)
        db.session.commit()
        print("Save user data to database, data: {}".format(self))
    # delete user data from database
    
    def delete_db(self):
        db.session.delete(self)
        db.session.commit()
        print("Delete user data from database, data: {}".format(self))

    # find by email
    def find_by_email(email):
        return db.query.filter_by(email=email).first()
    
    # find by active status
    def filter_by_active_status(is_active):
        return db.query.filter_by(is_active=is_active)
    
    # filter by content
    def filter_by_content(content):
        return db.query.filter_by(content=content).first()
    
    # count record
    def count_record(table, query):
        result = db[table].find(query).count()
        return result


    # ----------------------------------
    #   các tham số truyền vào :của hàm get_table 
    #   table => table
    #   query => câu lệnh truy vấn 
    #   order_by => sắp xếp theo 
    #   distinct => loại bỏ các bản ghi trùng trong table
    #   offset => số lượng trang
    #   limit => số object giới hạn mỗi offset
    #   incre => tự động phát sinh dữ liệu (tăng) mỗi khi dòng dữ liệu được chèn vào
    #   dont_get => update soon 
    # ----------------------------------
    # query by offset, limit
    def get_table(table, query, order_by=None, distinct=None, offset=None,
                 limit=None, incre=-1, dont_get=None):
        if offset is None:
            if limit is None:
                limit = 50
            offset = int(offset)
            limit = int(limit)
            if order_by:
                result = db[table].find(query, dont_get).sort(order_by, incre).skip(
                        (offset -1) * limit).limit(limit) 
            else:
                result = db[table].find(query, dont_get).skip(
                        (offset - 1) * limit).limit(
                        limit)
        else:
            if order_by:
                result = db[table].find(query, dont_get).sort(order_by, incre)
            else:
                result = db[table].find(query, dont_get)
            
        if type(distinct) is str:
            result = result.distinct(distinct)
            result = filter(lambda r: r != "", result)
        elif type(distinct) is dict:
            result = db[table].aggregate([
                {'$match': query},
                {
                    '$group': {
                        'id': distinct,
                    }
                }
            ]
            )

        if result:
            print("data return: {}".format(list(result)))
            return list(result)
        else:
            return []

                
    