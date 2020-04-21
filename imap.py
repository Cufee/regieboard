#!/usr/bin/env python3
#Function can recieve codes and links from mail server for verification
#Example  USAGE
#get_imap('<IMAP_SERVER>', '<IMAP_LOGIN>'', '<IMAP_PASSWORD>', '1vallie@gearage.ru', whattodo)
#print (get_imap('mail.ur30.ru', 'vallie@gearage.ru', 'jackwolf', '1vallie@gearage.ru', twitch_login_verify))

#WHATTODO
#1. twitch_reg_verify
#2. twitch_login_verify
#3. TBD


import imaplib
import pprint
import ssl
import email
import re
twitch_from_email = 'Twitch' #Twitch Sender name
riot_from_email = '' # RION Sender name
imap_folder = 'INBOX' # default for all mail servers


def get_imap(imap_server, imap_login, imap_pass, reg_email, whattodo):

    # Load system's trusted SSL certificates
    tls_context = ssl.create_default_context()
    # Connect (unencrypted at first)
    server = imaplib.IMAP4(imap_server)
    # Start TLS encryption. Will fail if TLS session can't be established
    server.starttls(ssl_context=tls_context)
    # Login. ONLY DO THIS AFTER server.starttls() !!
    server.login(imap_login, imap_pass)
    #Выбираем папку IMAP
    server.select(imap_folder, readonly=True)

    return whattodo(server,reg_email) # Вызываем функцию и что делать дальше.

def twitch_reg_verify(server,reg_email):
    try:
        #Ищем конкретные письма
        typ, data = server.uid ('search', None, 'TO {} FROM {} TEXT "Please verify your Twitch account."'.format(reg_email,twitch_from_email))
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
    
def twitch_login_verify(server,reg_email):
    try:
        #Ищем конкретные письма
        typ, data = server.uid ('search', None, 'TO {} FROM {} TEXT "Please enter the following code."'.format(reg_email,twitch_from_email))
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