#!/usr/bin/env python3
import imaplib
import pprint
import ssl
import email
import re
imap_login = 'vallie@gearage.ru'
imap_pass = 'jackwolf'
reg_email = '1vallie@gearage.ru'
from_email = "Twitch"
# Load system's trusted SSL certificates
tls_context = ssl.create_default_context()
# Connect (unencrypted at first)
server = imaplib.IMAP4('mail.ur30.ru')
# Start TLS encryption. Will fail if TLS session can't be established
server.starttls(ssl_context=tls_context)
# Login. ONLY DO THIS AFTER server.starttls() !!
server.login(imap_login, imap_pass)
#Выбираем папку IMAP
server.select('INBOX', readonly=True)


def twitch_reg_verify():
    try:
        #Ищем конкретные письма
        typ, data = server.uid ('search', None, 'TO {} FROM {} TEXT "Please verify your Twitch account."'.format(reg_email,from_email))
        latest_email_uid = data[0].split()[-1] # Получаем сроку номеров писем , Разделяем ID писем
        result, data = server.uid('fetch', latest_email_uid, '(RFC822)') # Получаем  письмо по rfc822
        raw_email = data[0][1].decode('utf-8') # вовзрашаем  письмо в UTF-8
        email_message = email.message_from_string(raw_email) # Засовывем писмо в либу для машинного чтения
        subject = (email_message['Subject']) #Twitch содержит код в Теме письма
        code_regex = re.findall(r'\d{6}', subject) # Проверяем subject на наш regexp
        code = code_regex[0] # Получаем код внутри найденого regex
    finally:
        try:
            server.close()
        except:
            pass

    return code
def twitch_login_verify():
    try:
        #Ищем конкретные письма
        typ, data = server.uid ('search', None, 'TO {} FROM {} TEXT "Please enter the following code."'.format(reg_email,from_email))
        latest_email_uid = data[0].split()[-1] # Получаем сроку номеров писем , Разделяем ID писем
        result, data = server.uid('fetch', latest_email_uid, '(RFC822)') # Получаем  письмо по rfc822
        raw_email = data[0][1].decode('utf-8') # вовзрашаем  письмо в UTF-8
        code_regex = re.findall(r'\>(\d{6})', raw_email) # Проверяем body на наш regexp
        code = code_regex[0]
    finally:
        try:
            server.close()
        except:
            pass
    return code

    #return code
print (twitch_login_verify())
# try:
#     #Выбираем папку IMAP
#     server.select('INBOX', readonly=True)
#     #Ищем конкретные письма
#     typ, data = server.uid ('search', None, 'TO {} FROM {} TEXT "Please verify your Twitch account."'.format(reg_email,from_email))
#     latest_email_uid = data[0].split()[-1] # Получаем сроку номеров писем , Разделяем ID писем
#     result, data = server.uid('fetch', latest_email_uid, '(RFC822)') # Получаем  письмо по rfc822
#     raw_email = data[0][1].decode('utf-8') # вовзрашаем  письмо в UTF-8
#     email_message = email.message_from_string(raw_email) # Засовывем писмо в либу для машинного чтения
#     subject = (email_message['Subject']) #Twitch содержит код в Теме письма
#     code_regex = re.findall(r'\d{6}', subject) # Проверяем subject на наш regexp
#     code = code_regex[0] # Получаем код внутри найденого regex
#     print("На нахуй код тебе от твича " + code)
# finally:
#     try:
#         server.close()
#     except:
#         pass
#     server.logout()

# Select mailbox
#server.select("INBOX")
#typ, msg_ids = server.search (
#           None, 'UNSEEN HEADER FROM "twitch.tv"'
#)
#print(msg_ids)
#print(msg_ids)
