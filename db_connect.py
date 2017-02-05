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

    # проверка наличия пользователя в базе с таким ИИН, если есть то записать ему telegram_user_id

    if foundUserWithINN(userInfo['tax_number'], userInfo['telegram_user_id']) == True:
        return True

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

def getUserInfo(userID):
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
        return userInfo[0]
    else:
        return False


def writeTaskNumber(userID, taskNumber):
    userInfo = getUserInfo(userID)

    if not userInfo:
        return

    try:
        db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
    except:
        return

    db.set_character_set("utf8")
    try:
        db.query("INSERT INTO UsersTasks (id, user_id, task_number) VALUE (null, '"+userInfo[0]+"', '"+taskNumber+"')")
    except:
        pass
    db.close()
    return

def getUserTasks(userID):
    try:
        db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
    except:
        return False

    db.set_character_set("utf8")
    try:
        db.query("SELECT userinfo.user_name, userstasks.task_number FROM userinfo LEFT JOIN userstasks ON userinfo.id = userstasks.user_id WHERE userinfo.telegram_user_id = "+str(userID)+";")
    except:
        return False
    resultQuery = db.use_result()
    taskList = resultQuery.fetch_row(0)
    db.close()
    return taskList
    # for task in taskList:
    #     print(task[1].decode('utf-8'))
    #
    # pass

# getUserTasks('165430624')


def foundUserWithINN(userINN, userID):
    try:
        db = _mysql.connect(host="localhost", user="root", passwd="q100689", db="ModernExpo")
    except BaseException as error:
        return str(error)

    db.set_character_set("utf8")
    try:
        db.query("SELECT * FROM UserInfo WHERE tax_number = " + str(userINN))
    except BaseException as error:
        return str(error)

    resultQuery = db.use_result()
    userInfo = resultQuery.fetch_row(0)

    if len(userInfo) == 0:
        db.close()
        return False

    id = userInfo[0][0]
    try:
        db.query("UPDATE UserInfo SET telegram_user_id = "+str(userID)+" WHERE UserInfo.id = "+str(id))
    except BaseException as error:
        return str(error)
    db.close()
    return True


