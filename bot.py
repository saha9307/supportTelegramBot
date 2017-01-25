import telebot
from jira import JIRA
import constants
import time

jira = JIRA(constants.jiraURL, basic_auth=(constants.jiraUser, constants.jiraPassword))

bot = telebot.TeleBot(constants.telegramBotToken)

usersRequestTaskInfo = {}
usersCreateTask = {}
descriptionNewTask = {}

@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, constants.strHello)

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, constants.strHelp)


# Get task info
# Start
@bot.message_handler(commands=['get_task_info'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    usersRequestTaskInfo[message.chat.id] = constants.USER_GET_TASK_INFO
    bot.send_message(message.from_user.id, constants.strGetTaskInfo)

@bot.message_handler(func=lambda message: usersRequestTaskInfo.get(message.chat.id) == constants.USER_GET_TASK_INFO)
def get_task_info(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    try:
        issue = jira.issue(message.text.upper())

        status = issue.fields.status.name
        if issue.fields.status.name == constants.strDone:
            status = 'Готово'
        elif issue.fields.status.name == constants.strToDo:
            status = 'До виконання'
        elif issue.fields.status.name == constants.strInProgress:
            status = 'В роботі'

        bot.send_message(message.from_user.id, 'Задача: ' + issue.fields.summary +
                         '\nСтатус: ' + status +
                         '\nІніціатор: ' + issue.fields.creator.displayName +
                         '\nВиконавець: ' + issue.fields.assignee.displayName)
    except Exception as err:
        bot.send_message(message.from_user.id, constants.strTaskNotFound);
        pass
    usersRequestTaskInfo[message.chat.id] = False

#
# End Set Task Info


# Start Create new task
@bot.message_handler(commands=['set_new_task'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    usersCreateTask[message.chat.id] = constants.USER_SET_NEW_TASK
    bot.send_message(message.from_user.id, constants.strCreateNewTask)

@bot.message_handler(func=lambda message: usersCreateTask.get(message.chat.id) == constants.USER_SET_NEW_TASK)
def get_task_info(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    # Code for create new task in Jira System
    new_issue = jira.create_issue(project='SUP', summary='New issue from jira-python',
                                  description='Look into this one', issuetype={'name': 'Bug'})
    bot.send_message(message.from_user.id, new_issue.id)
    time.sleep(2)


# End Create new task




@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, message.text)


bot.polling(none_stop=True, interval=0)
