import telebot
from jira import JIRA
import constants
import db_connect
import json
import requests
import os



jira = JIRA(constants.jiraURL, basic_auth=(constants.jiraUser, constants.jiraPassword))

bot = telebot.TeleBot(constants.telegramBotToken)

usersRequestTaskInfo = {}
usersCreateTask = {}
descriptionNewTask = {}

usersLastTask = {}
userSetFile = {}

userRegistration = {}

def userVerification(userID):
    userRegistered = db_connect.userRegistered(userID)
    if not userRegistered:
        bot.send_message(userID, 'Для використання бота, пройдіть реєстрацію')
        bot.send_message(userID, 'Що б зареєструватись, натисніть /registration')
        return False
    elif isinstance(userRegistered, str):
        bot.send_message(userID, 'Виникла помилка у роботі бота. Спробуйте пізніше. Ми працюм над усуненням проблеми')
        bot.send_message(userID, userRegistered)
        # відправити ще на мене повідомлення про помилку
        bot.send_message(165430624, userRegistered)
        return False
    return True

def registrNewUser(userID):
    bot.send_chat_action(userID, 'typing')
    userRegistration[userID] = constants.REGISTRATION_NEW_USER
    bot.send_message(userID, constants.strRegistrationNewUser)

def getUserInfoFrom1C(userINN, userID):
    url = 'http://212.1.103.131/BaseCRM/hs/WebModern/GetUserInfo?session=87a95fsfc-063d-482c-8687-6c95733eec9d'
    headers = {'Content-Type': "application/json"}
    data = {"INN": str(userINN)}
    jdata = json.dumps(data).encode('utf8')
    res = requests.post(url, auth=('Администратор'.encode('utf-8'), ''), data=jdata, headers=headers)

    if res.status_code == 200:
        return json.loads(res.text)
    elif res.status_code == 404:
        bot.send_message(userID, 'Користувач із вказаним податковим номером не знайдений в базі Modern-Expo')
        return False
    else:
        bot.send_message(userID,
                         'Виникла помилка у роботі бота. Вибачте за тимчасовы незручності. Ми працюєм над усуненням проблеми.')
        # відправити ще на мене повідомлення про помилку
        bot.send_message(165430624, str(res.status_code)+'\n' + str(res.text))
        return False





@bot.message_handler(commands=['registration'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    registrNewUser(message.from_user.id)


@bot.message_handler(func=lambda message: userRegistration.get(message.chat.id) == constants.REGISTRATION_NEW_USER)
def get_user_inn(message):
    userSetFile[message.chat.id] = False
    userINN = message.text.upper().replace(' ', '')
    if userINN == '':
        bot.send_message(message.from_user.id, 'ІНН не можу бути пустим. Спробуйте знову.')
        userRegistration[message.chat.id] = False
        return
    userInfo = getUserInfoFrom1C(userINN, message.chat.id)
    if userInfo == False or userInfo == '404':
        bot.send_message(message.chat.id, 'Користувач із вказаним податковим номером не знайдений в базі Modern-Expo')
        bot.send_message(message.chat.id, 'Для використання бота, пройдіть реєстрацію')
        bot.send_message(message.chat.id, 'Що б зареєструватись, натисніть /registration')
        userRegistration[message.chat.id] = False
        return

    userInfo['telegram_user_id'] = message.from_user.id
    userInfo['tax_number'] = userINN
    result = db_connect.writeNewUser(userInfo)
    if isinstance(result, str):
        bot.send_message(message.from_user.id,
                         'Виникла помилка у роботі бота. Спробуйте пізніше. Ми працюм над усуненням проблем')
        bot.send_message(message.from_user.id, result)
        # відправити ще на мене повідомлення про помилку
        bot.send_message(165430624, result)

    bot.send_message(message.from_user.id, 'Вітаємо з успішною реєстрацією')
    markup = telebot.types.ReplyKeyboardMarkup(True, False)
    markup.row('/new_task', '/task_info', '/task_list')
    markup.row('/help')
    bot.send_message(message.from_user.id, "Виберіть необхідну функцію:", reply_markup=markup)
    userRegistration[message.chat.id] = False



@bot.message_handler(commands=['start'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, constants.strHello)

    userRegistered = db_connect.userRegistered(message.from_user.id)
    if not userRegistered:
        registrNewUser(message.from_user.id)
    elif isinstance(userRegistered, str):
        bot.send_message(message.from_user.id, 'Виникла помилка у роботі бота. Спробуйте пізніше. Ми працюм над усуненням проблеми')
        bot.send_message(message.from_user.id, userRegistered)
        # відправити ще на мене повідомлення про помилку
        bot.send_message(165430624, userRegistered)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(True, False)
        markup.row('/new_task', '/task_info', '/task_list')
        markup.row('/help')
        bot.send_message(message.from_user.id, "Виберіть необхідну функцію:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, constants.strHelp)


# Get task info ====================================================
# Start
@bot.message_handler(commands=['task_info'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    if not userVerification(message.from_user.id):
        return
    bot.send_chat_action(message.from_user.id, 'typing')
    usersRequestTaskInfo[message.chat.id] = constants.USER_GET_TASK_INFO
    bot.send_message(message.from_user.id, constants.strGetTaskInfo)

@bot.message_handler(func=lambda message: usersRequestTaskInfo.get(message.chat.id) == constants.USER_GET_TASK_INFO)
def get_task_info(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    try:
        issue = jira.issue(message.text.upper())
        # #bot.send_message(message.from_user.id, issue.key)
        status = issue.fields.status.name
        if issue.fields.status.name == constants.strDone:
            status = 'Готово'
        elif issue.fields.status.name == constants.strToDo:
            status = 'До виконання'
        elif issue.fields.status.name == constants.strInProgress:
            status = 'В роботі'

        comments = ''
        for comment in issue.fields.comment.comments:
            comments += '\n ' + comment.author.displayName + ':\n  ' + comment.body

        bot.send_message(message.from_user.id, 'Задача: ' + issue.fields.description +
                         '\nСтатус: ' + status +
                         '\nІніціатор: ' + issue.fields.creator.displayName +
                         '\nВиконавець: ' + issue.fields.assignee.displayName+
                         '\nКоментарі: ' + comments)
    except Exception as err:
        bot.send_message(message.from_user.id, constants.strTaskNotFound);
    usersRequestTaskInfo[message.chat.id] = False
# End Set Task Info=================================================


# Start Create new task=============================================
@bot.message_handler(commands=['new_task'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    if not userVerification(message.from_user.id):
        return
    bot.send_chat_action(message.from_user.id, 'typing')
    usersCreateTask[message.chat.id] = constants.USER_SET_NEW_TASK
    bot.send_message(message.from_user.id, constants.strCreateNewTask)

@bot.message_handler(func=lambda message: usersCreateTask.get(message.chat.id) == constants.USER_SET_NEW_TASK)
def create_new_task(message):
    bot.send_chat_action(message.from_user.id, 'typing')

    userInfo = db_connect.getUserInfo(message.from_user.id)
    if not userInfo:
        return

    # Code for create new task in Jira System
    summary = message.text + '\nКористувач Telegram: ' + message.from_user.first_name + ' ' + message.from_user.last_name
    summary += '\nКлієнт: ' + userInfo[1].decode('utf-8')
    if userInfo[2].decode('utf-8') != 'None' and userInfo[2].decode('utf-8') != '':
        summary += '\nВнутр.Тел.: ' + userInfo[2].decode('utf-8')

    if userInfo[3].decode('utf-8') != 'None' and userInfo[3].decode('utf-8') != '':
        summary += '\nМоб.Тел.: ' + userInfo[3].decode('utf-8')

    if userInfo[4].decode('utf-8') != 'None' and userInfo[4].decode('utf-8') != '':
        summary += '\nEmail: ' + userInfo[4].decode('utf-8')

    new_issue = jira.create_issue(project='SUP', summary=message.text,
                                  description=summary, issuetype={'name': 'Bug'}, assignee={'name':'JiraSupport'})
    bot.send_message(message.from_user.id, 'Номер вашого звернення: ' + new_issue.key)
    usersCreateTask[message.chat.id] = False
    db_connect.writeTaskNumber(message.chat.id, new_issue.key)
    usersLastTask[message.chat.id] = str(new_issue.key)
    userSetFile[message.chat.id] = constants.SET_FILE_USER
# End Create new task===============================================


@bot.message_handler(commands=['task_list'])
def get_task_list(message):
    userSetFile[message.chat.id] = False
    bot.send_chat_action(message.from_user.id, 'typing')
    taskList = db_connect.getUserTasks(message.from_user.id)

    if taskList == False:
        return
    strTask = 'Список Ваших задач:'
    for task in taskList:
        if task[1] == None:
            continue
        strTask += '\n' + task[1].decode('utf-8')

    bot.send_message(message.from_user.id, strTask)

@bot.message_handler(content_types=['document'], func=lambda message: userSetFile.get(message.chat.id) == constants.SET_FILE_USER)
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')

    taskNumber = usersLastTask[message.chat.id]

    if taskNumber == '':
        return

    file_info = bot.get_file(message.document.file_id)

    issue = jira.issue(id=taskNumber)

    with open(file_info.file_path, "wb") as file:
        response = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(constants.telegramBotToken, file_info.file_path))
        file.write(response.content)

    jira.add_attachment(issue=issue, attachment=file_info.file_path)
    userSetFile[message.chat.id] = False
    bot.send_message(message.from_user.id, 'Файл прикліплений до задачі ' + str(taskNumber))
    try:
        os.remove(file_info.file_path)
    except:
        pass



@bot.message_handler(content_types=['text'])
def handle_text(message):
    userSetFile[message.chat.id] = False
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, message.text+' '+str(type(message.from_user.id)))

bot.polling(none_stop=True, interval=0)
