import _mysql
ERROR = ''

def userRegistered(userID):
    try:
        db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
    except BaseException as error:
        return str(error)

    db.set_character_set("utf8")
    db.query("SELECT * FROM UserInfo WHERE telegram_user_id = " + str(userID))
    resultQuery = db.use_result()
    userInfo = resultQuery.fetch_row(0)
    db.close()
    if len(userInfo) > 0:
        return True
    else:
        return False


def writeNewUser(userInfo):
    try:
        db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
    except BaseException as error:
        return str(error)

    db.set_character_set("utf8")
    try:
        db.query("INSERT INTO UserInfo (id, user_name, work_phone, mobile_number, email, tax_number, telegram_user_id) VALUES (null, '"+str(userInfo['user_name'])+"', '"+str(userInfo['work_phone'])+"', '"+str(userInfo['mobile_number'])+"', '"+str(userInfo['email'])+"', '"+str(userInfo['tax_number'])+"', '" +str(userInfo['telegram_user_id'])+"')")
        db.close()
        return True
    except BaseException as error:
        return str(error)
