import os,time, asyncio
from lib import Facebook
from lib import response
from colorama import Fore,Back,Style
from concurrent.futures import ThreadPoolExecutor


banner = f"""
{Fore.BLUE}        ╔═╗╦╔═╗╔╗ 
        ╠═╣║╠╣ ╠╩╗
        ╩ ╩╩╚  ╚═╝{Fore.RESET}
      [{Back.LIGHTBLUE_EX}{Fore.WHITE} AI FACEBOOK {Fore.RESET}{Back.RESET}]

{Fore.LIGHTMAGENTA_EX}⟶{Fore.RESET} Author   : {Fore.GREEN}Jhosua{Fore.RESET}
{Fore.LIGHTMAGENTA_EX}⟶{Fore.RESET} Facebook : {Fore.GREEN}facebook.com/kzdgzr{Fore.RESET}
{Fore.LIGHTMAGENTA_EX}⟶{Fore.RESET} Github   : {Fore.GREEN}github.com/KZREVOXTICAL{Fore.RESET}
"""

fb = Facebook()


async def main():
    t = 0
    if fb.validate:
        q = input(f'[{Fore.GREEN}1{Fore.RESET}]. Start' + \
            f'\n[{Fore.RED}0{Fore.RESET}]. Logout' + \
            '\n\nOption > '
        )
        if q == "0" or q == "00":
            os.remove('.cookie.log');exit()

        os.system('clear')
        print(banner)
        print(f'------------[ {Fore.WHITE}MENUNGGU PESAN{Fore.RESET} ]------------')
        while True:
            try:
                msg = await fb.get_message()
                if msg != None:
                    print(f"[{Fore.GREEN}{msg.name}{Fore.RESET}] : {msg.body}")
                    t+=1
                    print(f"=> Total Pesan : ({Fore.LIGHTYELLOW_EX}{t}{Fore.RESET})",end="\r")
                    
                    # Response
                    response_ai = await response(msg.body)
                    await fb.send_message(msg.to,msg.data,response_ai)
            
            except Exception as e:
                print(f"[{Fore.RED}ERROR{Fore.RESET}] {e}")
        
    else:
        print(f"[{Fore.RED}!{Fore.RESET}] Login Gagal :(")
        os.remove('.cookie.log')


if __name__ == "__main__":

    os.system("clear")
    print(banner)
    if os.path.exists('.cookie.log'):
        fb.set_cookie = open('.cookie.log').read()
        asyncio.run(main())
        
    if not os.path.exists('.cookie.log'):
        fc = open('.cookie.log','w')
        cookie = input(f'[{Fore.GREEN}?{Fore.RESET}] Cookie : ')
        fc.write(cookie)
        fc.close()
        print(f'[{Fore.GREEN}!{Fore.RESET}] Silahkan jalankan ulang script ini!')
