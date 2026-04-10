from tkinter import *
import os 
import json
import pygame

py_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(py_dir, "save.json")


money = float(0)

upgrade_cost = float(1.5)
upgrade_cost_passive = float(.75)
upgrade_level = 0
upgrade_level_passive = 0

count = 0
click_power = float(.01)
passive_income = 0

window = Tk()
window.title("Click!")


photo = PhotoImage(file=os.path.join(py_dir, "pfp.png"))
bg = PhotoImage(file=os.path.join(py_dir, "background.png"))
window.iconphoto(True, photo)

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(py_dir, "background_music.mp3"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

is_muted = False
volume = 0.3


def save_game():
    data = {
        "money": money,
        "count": count,
        "click_power": click_power,
        "passive_income": passive_income,
        "upgrade_level": upgrade_level,
        "upgrade_level_passive": upgrade_level_passive,
        "upgrade_cost": upgrade_cost,
        "upgrade_cost_passive": upgrade_cost_passive
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved!")

def load_game():
    global money, count, click_power, passive_income
    global upgrade_level, upgrade_level_passive, upgrade_cost, upgrade_cost_passive

    if not os.path.exists(SAVE_FILE):
        print("No save file found, starting fresh.")
        return

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    money = data["money"]
    count = data["count"]
    click_power = data["click_power"]
    passive_income = data["passive_income"]
    upgrade_level = data["upgrade_level"]
    upgrade_level_passive = data["upgrade_level_passive"]
    upgrade_cost = data["upgrade_cost"]
    upgrade_cost_passive = data["upgrade_cost_passive"]
    print("Game loaded!")

def load_ui():
    label.config(text=(f"${money:.2f}"))
    purchase_button.config(text=f"Purchase Click Upgrade: ${upgrade_cost:.2f}")
    purchase_button_passive.config(text=f"Purchase Passive Upgrade: ${upgrade_cost_passive:.2f}")
    current_power.config(text=(f"$ Per Click: ${click_power:.2f}"))
    money_per_sec.config(text=(f"$ Per Second: ${passive_income:.3f}"))

def autosave():
    save_game()
    window.after(30000, autosave) 

def toggle_mute():
    global is_muted, volume
    if is_muted:
        pygame.mixer.music.set_volume(volume)
        mute_button.config(text="🔊")
    else:
        pygame.mixer.music.set_volume(0)
        mute_button.config(text="🔇")
    is_muted = not is_muted

def change_volume(val):
    global volume, is_muted
    volume = float(val)
    if not is_muted:
        pygame.mixer.music.set_volume(volume)

def click():
    global count, money
    count += 1
    money +=  click_power
    print(f"Money: ${money:.2f} | Clicks: {count}")
    label.config(text=(f"$:{money:.2f}"))

def purchase_upgrade():
    global money, upgrade_cost, upgrade_level, click_power
    if money >= upgrade_cost:
        money -= upgrade_cost
        upgrade_level += 1
        click_power = float(0.01 * (upgrade_level ** 0.6 + 1))
        upgrade_cost = float(1.5 * (1.2 ** upgrade_level))
        purchase_button.config(text=f"Purchase Upgrade: ${upgrade_cost:.2f}")
        label.config(text=(f"$:{money:.2f}"))
        current_power.config(text=(f"$ Per Click: ${float(click_power):.2f}"))
        print(f"Upgrade purchased! Multiplier: {click_power}x | Next upgrade: {upgrade_cost:.2f}")
    else:
        print(f"Not enough money! Need {upgrade_cost}, have {money}")

def purchase_upgrade_passive():
    global money, upgrade_cost_passive, upgrade_level_passive, passive_income
    if money >= upgrade_cost_passive:
        money -= upgrade_cost_passive
        upgrade_level_passive += 1
        passive_income = float(0.005 * (upgrade_level_passive ** 0.5 + 1))
        upgrade_cost_passive = float(0.75 * (1.14 ** upgrade_level_passive))
        purchase_button_passive.config(text=f"Purchase Passive Income: ${upgrade_cost_passive:.2f}")
        label.config(text=(f"$: {money:.2f}"))
        money_per_sec.config(text=(f"$ Per Second: ${float(passive_income):.3f}"))
        print(f"Upgrade purchased! Passive Income: {passive_income}x | Next upgrade: {upgrade_cost_passive:.2f}")
    else:
        print(f"Not enough money! Need {upgrade_cost_passive}, have {money}")
    
def money_per_second():
    global money
    money += passive_income
    label.config(text=(f"$:{money:.2f}"))
    window.after(1000, money_per_second)

def on_close():
    save_game()
    pygame.mixer.music.stop()
    pygame.quit()
    window.destroy()

save_button = Button(window, 
                     command=save_game, 
                     text="Save", 
                     height=1, 
                     width=5,
                     fg="#54DB2B",
                     bg="#2F3A68")

load_button = Button(window, 
                     command=load_game, 
                     text="Load", 
                     height=1, 
                     width=5,
                     fg="#54DB2B",
                     bg="#2F3A68")

button = Button(window,
                command=click,
                state=ACTIVE,
                image=photo,
                compound='bottom',
                height=300,
                width=400,
                justify=CENTER)

label = Label(text=(f"${money:.2f}"),
              font=('Monospace', 30),
              fg="#54DB2B",
              bg='#2F3A68',
              height=1,
              width=10)

purchase_button = Button(window, 
                command=purchase_upgrade,
                text=(f"Purchase Click Upgrade: ${float(upgrade_cost):.2f}"),
                bg="#F1A991")

purchase_button_passive = Button(command=purchase_upgrade_passive,
                text=(f"Purchase Passive Upgrade: ${float(upgrade_cost_passive):.2f}"),
                bg="#F1A991")

current_power = Label(text=(f"$ Per Click: ${float(click_power):.2f}"),
                      bg="#F1A991")

money_per_sec = Label(text=(f"$ Per Second: ${float(passive_income):.3f}"),
                      bg="#F1A991")

volume_slider = Scale(window, 
                      from_=0, 
                      to=1, 
                      resolution=0.01, 
                      orient=HORIZONTAL,
                      command=change_volume, 
                      length=120, 
                      showvalue=False,
                      bg="#2F3A68")

volume_slider.set(0.3)

mute_button = Button(window, 
                     text="🔊", 
                     command=toggle_mute, 
                     width=3)

window.columnconfigure(0, weight=1, minsize=200)
window.columnconfigure(1, weight=1, minsize=200)
window.columnconfigure(2, weight=1, minsize=200)

label.grid(row=0, column=0, columnspan=3, pady=10)

save_button.grid(row=0, column=0, sticky='e', padx=10)
load_button.grid(row=0, column=2, sticky='w', padx=10)
mute_button.grid(row=1, column=0, sticky='w', padx=(10,0), pady=4)
volume_slider.grid(row=1, column=0, sticky='w', padx=(40,0), pady=4)

button.grid(row=2, column=0, columnspan=3, pady=10)

purchase_button.grid(row=3, column=0, sticky='w', padx=10, pady=2)
purchase_button_passive.grid(row=4, column=0, sticky='w', padx=10, pady=2)

current_power.grid(row=3, column=2, sticky='e', padx=10, pady=2)
money_per_sec.grid(row=4, column=2, sticky='e', padx=10, pady=2)


window.geometry("900x600")
window.resizable(False, False)

label1 = Label(window, image=bg)
label1.place(x=0, y=0, relwidth=1, relheight=1)
label1.lower() 

load_game()
load_ui()

autosave()
money_per_second()
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()