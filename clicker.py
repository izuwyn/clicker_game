from tkinter import *
import os 
import json

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

photo = PhotoImage(file=os.path.join(py_dir, "pfp.png"))

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
    money_per_sec.config(text=(f"$ Per Second (Passive Upgrades): ${passive_income:.3f}"))

def autosave():
    save_game()
    window.after(30000, autosave) 

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
        money_per_sec.config(text=(f"$ Per Second (Passive Upgrades): ${float(passive_income):.3f}"))
        print(f"Upgrade purchased! Passive Income: {passive_income}x | Next upgrade: {upgrade_cost_passive:.2f}")
    else:
        print(f"Not enough money! Need {upgrade_cost_passive}, have {money}")
    
def money_per_second():
    global money
    money += passive_income
    label.config(text=(f"$:{money:.2f}"))
    window.after(1000, money_per_second)

save_button = Button(window, command=save_game, text="Save")

load_button = Button(window, command=load_game, text="Load")

button = Button(window,
                text="Click me!",
                command=click,
                font=("Comic Sans", 30),
                fg="#00FF00",
                bg="black",
                activeforeground="#00FF00",
                activebackground="black",
                state=ACTIVE,
                image=photo,
                compound='bottom',
                height=50,
                width=50)

label = Label(text=(f"${money:.2f}"),
              font=('Monospace', 50))

purchase_button = Button(window, 
                command=purchase_upgrade,
                text=(f"Purchase Click Upgrade: ${float(upgrade_cost):.2f}"))

purchase_button_passive = Button(command=purchase_upgrade_passive,
                text=(f"Purchase Passive Upgrade: ${float(upgrade_cost_passive):.2f}"))

current_power = Label(text=(f"$ Per Click: ${float(click_power):.2f}"))

money_per_sec = Label(text=(f"$ Per Second (Passive Upgrades): ${float(passive_income):.3f}"))


label.pack()
button.pack()
purchase_button.pack()
purchase_button_passive.pack()
current_power.pack()
money_per_sec.pack()
save_button.pack()
load_button.pack()

load_game()
load_ui()

autosave()
money_per_second()
window.mainloop()