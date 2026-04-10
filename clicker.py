import customtkinter as ctk
from tkinter import *
from PIL import Image
import os 
import json
import pygame

# Patch for backward compatibility
ctk.CTkLabel.config = ctk.CTkLabel.configure
ctk.CTkButton.config = ctk.CTkButton.configure

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

py_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(py_dir, "save.json")


money = float(0)

upgrade_cost = float(1.5)
upgrade_cost_passive = float(.75)
upgrade_level = 0
upgrade_level_passive = 0
total_money = float(0)
total_gems = float(0)
total_tokens = float(0)

count = 0
click_power = float(.01)
passive_income = 0
prestige_level = 0
prestige_cost = float(1000)

gems = 0
tokens = 0
gem_upgrade_cost = 10.0
token_upgrade_cost = 10.0
gem_upgrade_level = 0
token_upgrade_level = 0

window = ctk.CTk()
window.title("Modern Clicker Dashboard")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

pfp_img = Image.open(os.path.join(py_dir, "pfp.png"))
photo = ctk.CTkImage(light_image=pfp_img, dark_image=pfp_img, size=(220, 220))

gem_img = Image.open(os.path.join(py_dir, "gem_icon.png"))
gem_photo = ctk.CTkImage(light_image=gem_img, dark_image=gem_img, size=(220, 220))

money_img = Image.open(os.path.join(py_dir, "money_icon.png"))
money_photo = ctk.CTkImage(light_image=money_img, dark_image=money_img, size=(220, 220))

token_img = Image.open(os.path.join(py_dir, "token_icon.png"))
token_photo = ctk.CTkImage(light_image=token_img, dark_image=token_img, size=(220, 220))

try:
    bg_img = Image.open(os.path.join(py_dir, "background.png"))
    bg = ctk.CTkImage(light_image=bg_img, dark_image=bg_img, size=(screen_width, screen_height))
    
    icon_photo = PhotoImage(file=os.path.join(py_dir, "pfp.png"))
    window.iconphoto(True, icon_photo)
except:
    pass

pygame.mixer.init()
pygame.mixer.music.load(os.path.join(py_dir, "background_music.mp3"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

buy_sound = pygame.mixer.Sound(os.path.join(py_dir, "purchase.mp3"))
buy_sound.set_volume(0.4)

no_buy_sound = pygame.mixer.Sound(os.path.join(py_dir, "no_purchase.mp3"))
no_buy_sound.set_volume(0.6)

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
        "upgrade_cost_passive": upgrade_cost_passive,
        "total_money": total_money,
        "prestige_level": prestige_level,
        "prestige_cost": prestige_cost,
        "gems": gems,
        "tokens": tokens,
        "gem_upgrade_cost": gem_upgrade_cost,
        "token_upgrade_cost": token_upgrade_cost,
        "gem_upgrade_level": gem_upgrade_level,
        "token_upgrade_level": token_upgrade_level,
        "total_gems": total_gems,
        "total_tokens": total_tokens
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("Game saved!")

def load_game():
    global money, count, click_power, passive_income, total_money
    global upgrade_level, upgrade_level_passive, upgrade_cost, upgrade_cost_passive
    global prestige_level, prestige_cost
    global gems, tokens, gem_upgrade_cost, token_upgrade_cost, gem_upgrade_level, token_upgrade_level
    global total_gems, total_tokens

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
    total_money = data["total_money"]
    prestige_level = data.get("prestige_level", 0)
    prestige_cost = data.get("prestige_cost", 1000.0)
    gems = data.get("gems", 0.0)
    tokens = data.get("tokens", 0.0)
    gem_upgrade_cost = data.get("gem_upgrade_cost", 10.0)
    token_upgrade_cost = data.get("token_upgrade_cost", 10.0)
    gem_upgrade_level = data.get("gem_upgrade_level", 0)
    token_upgrade_level = data.get("token_upgrade_level", 0)
    total_gems = data.get("total_gems", 0.0)
    total_tokens = data.get("total_tokens", 0.0)
    print("Game loaded!")

def update_counters():
    label.config(text=f"${money:.2f}")
    if 'gem_label' in globals():
        gem_label.config(text=f"💎 {gems:.0f}")
        token_label.config(text=f"🪙 {tokens:.0f}")
        total_money_label.config(text=f"Total Earned: ${float(total_money):.3f}")
        total_gems_label.config(text=f"Total Gems: 💎 {float(total_gems):.0f}")
        total_tokens_label.config(text=f"Total Tokens: 🪙 {float(total_tokens):.0f}")

def update_powers():
    global click_power, passive_income
    base_click = 0.01 * (upgrade_level ** 0.9 + 1)
    click_power = base_click * (gem_upgrade_level * 2.0 + 1.0)
    base_passive = 0.01 * (upgrade_level_passive ** 0.65 + 1)
    passive_income = base_passive * (token_upgrade_level * 2.0 + 1.0)

def load_ui():
    update_counters()
    purchase_button.config(text=f"Click Upgrade: ${upgrade_cost:.2f}")
    purchase_button_passive.config(text=f"Passive Upgrade: ${upgrade_cost_passive:.2f}")
    if 'gem_upgrade_btn' in globals():
        gem_upgrade_btn.config(text=f"Gem Upgrade (Power x{gem_upgrade_level*2+1}): 💎 {gem_upgrade_cost:.1f}")
        token_upgrade_btn.config(text=f"Token Upgrade (Passive x{token_upgrade_level*2+1}): 🪙 {token_upgrade_cost:.1f}")
    current_power.config(text=f"$ Per Click: ${click_power * (2.0 ** prestige_level):.3f}")
    money_per_sec.config(text=f"$ Per Second: ${passive_income * (2.0 ** prestige_level):.3f}")
    prestige_button.config(text=f"Prestige (x{2.0 ** prestige_level}): ${prestige_cost:.2f}")
    prestige_label.config(text=f"Prestige Level: {prestige_level}")

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
    global count, money, total_money
    count += 1
    mult = 2.0 ** prestige_level
    gained = click_power * mult
    money += gained
    total_money += gained
    update_counters()

def click_gems():
    global gems, total_gems
    mult = 2.0 ** prestige_level
    gained = 1 * mult
    gems += gained
    total_gems += gained
    update_counters()

def click_tokens():
    global tokens, total_tokens
    mult = 2.0 ** prestige_level
    gained = 1 * mult
    tokens += gained
    total_tokens += gained
    update_counters()

def purchase_upgrade():
    global money, upgrade_cost, upgrade_level
    if money >= upgrade_cost:
        money -= upgrade_cost
        upgrade_level += 1
        buy_sound.play()
        update_powers()
        upgrade_cost = float(1.5 * (1.2 ** upgrade_level))
        purchase_button.config(text=f"Click Upgrade: ${upgrade_cost:.2f}")
        update_counters()
        current_power.config(text=f"$ Per Click: ${click_power * (2.0 ** prestige_level):.3f}")
        print(f"Upgrade purchased! Next upgrade: {upgrade_cost:.3f}")
    else:
        no_buy_sound.play()
        print(f"Not enough money! Need {upgrade_cost}, have {money}")

def purchase_upgrade_passive():
    global money, upgrade_cost_passive, upgrade_level_passive
    if money >= upgrade_cost_passive:
        money -= upgrade_cost_passive
        upgrade_level_passive += 1
        buy_sound.play()
        update_powers()
        upgrade_cost_passive = float(0.75 * (1.14 ** upgrade_level_passive))
        purchase_button_passive.config(text=f"Passive Upgrade: ${upgrade_cost_passive:.2f}")
        update_counters()
        money_per_sec.config(text=f"$ Per Second: ${passive_income * (2.0 ** prestige_level):.3f}")
        print(f"Upgrade purchased! Next upgrade: {upgrade_cost_passive:.3f}")
    else:
        no_buy_sound.play()
        print(f"Not enough money! Need {upgrade_cost_passive}, have {money}")

def purchase_gem_upgrade():
    global gems, gem_upgrade_cost, gem_upgrade_level
    if gems >= gem_upgrade_cost:
        gems -= gem_upgrade_cost
        gem_upgrade_level += 1
        buy_sound.play()
        update_powers()
        gem_upgrade_cost = float(10.0 * (1.5 ** gem_upgrade_level))
        gem_upgrade_btn.config(text=f"Gem Upgrade (Power x{gem_upgrade_level*2+1}): 💎 {gem_upgrade_cost:.1f}")
        update_counters()
        current_power.config(text=f"$ Per Click: ${click_power * (2.0 ** prestige_level):.3f}")
        print(f"Gem Upgrade purchased!")
    else:
        no_buy_sound.play()
        print(f"Not enough gems! Need {gem_upgrade_cost}, have {gems}")

def purchase_token_upgrade():
    global tokens, token_upgrade_cost, token_upgrade_level
    if tokens >= token_upgrade_cost:
        tokens -= token_upgrade_cost
        token_upgrade_level += 1
        buy_sound.play()
        update_powers()
        token_upgrade_cost = float(10.0 * (1.5 ** token_upgrade_level))
        token_upgrade_btn.config(text=f"Token Upgrade (Passive x{token_upgrade_level*2+1}): 🪙 {token_upgrade_cost:.1f}")
        update_counters()
        money_per_sec.config(text=f"$ Per Second: ${passive_income * (2.0 ** prestige_level):.3f}")
        print(f"Token Upgrade purchased!")
    else:
        no_buy_sound.play()
        print(f"Not enough tokens! Need {token_upgrade_cost}, have {tokens}")

def purchase_prestige():
    global money, prestige_cost, prestige_level
    if money >= prestige_cost:
        money -= prestige_cost
        prestige_level += 1
        buy_sound.play()
        prestige_cost = float(1000.0 * (10.0 ** prestige_level))
        prestige_button.config(text=f"Prestige (x{2.0 ** prestige_level}): ${prestige_cost:.2f}")
        prestige_label.config(text=f"Prestige Level: {prestige_level}")
        update_counters()
        current_power.config(text=f"$ Per Click: ${click_power * (2.0 ** prestige_level):.3f}")
        money_per_sec.config(text=f"$ Per Second: ${passive_income * (2.0 ** prestige_level):.3f}")
        print(f"Prestige purchased! Level: {prestige_level}")
    else:
        no_buy_sound.play()
        print(f"Not enough money! Need {prestige_cost}, have {money}")

def money_per_second():
    global money, total_money
    mult = 2.0 ** prestige_level
    gained = passive_income * mult
    money += gained
    total_money += gained
    update_counters()
    window.after(1000, money_per_second)

def on_close():
    save_game()
    pygame.mixer.music.stop()
    pygame.quit()
    window.destroy()

# BACKGROUND LAYER
background_image_obj = ctk.CTkLabel(window, image=bg, text="")
background_image_obj.place(x=0, y=0, relwidth=1, relheight=1)
background_image_obj.lower()

# TOP DASHBOARD
top_frame = ctk.CTkFrame(window, fg_color="#181820", corner_radius=15, border_width=1, border_color="#2A2A35")
top_frame.pack(fill="x", pady=15, padx=20)

stats_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
stats_frame.pack(side="top", pady=10)

gem_label = ctk.CTkLabel(stats_frame, text=f"💎 {gems:.0f}", font=('Montserrat', 35, 'bold'), text_color="#2BC8FF")
gem_label.pack(side="left", padx=30)

label = ctk.CTkLabel(stats_frame, text=f"${money:.2f}", font=('Montserrat', 50, 'bold'), text_color="#00E676")
label.pack(side="left", padx=30)

token_label = ctk.CTkLabel(stats_frame, text=f"🪙 {tokens:.0f}", font=('Montserrat', 35, 'bold'), text_color="#FFD700")
token_label.pack(side="left", padx=30)

header_controls = ctk.CTkFrame(top_frame, fg_color="transparent")
header_controls.pack(pady=(0, 15))

save_button = ctk.CTkButton(header_controls, command=save_game, text="Save", width=90, corner_radius=12, fg_color="#2A2A35", hover_color="#3A3A4A")
save_button.pack(side="left", padx=8)

load_button = ctk.CTkButton(header_controls, command=load_game, text="Load", width=90, corner_radius=12, fg_color="#2A2A35", hover_color="#3A3A4A")
load_button.pack(side="left", padx=8)

mute_button = ctk.CTkButton(header_controls, text="🔊", command=toggle_mute, width=40, fg_color="#2A2A35", hover_color="#3A3A4A")
mute_button.pack(side="left", padx=8)

volume_slider = ctk.CTkSlider(header_controls, from_=0, to=1, command=change_volume, width=120, button_color="#00E676", button_hover_color="#00C853")
volume_slider.set(0.3)
volume_slider.pack(side="left", padx=10)

# CARDS AREA
center_frame = ctk.CTkFrame(window, fg_color="transparent")
center_frame.pack(expand=True)

button1 = ctk.CTkButton(center_frame, text="Farm Gems\n💎💎💎", font=('Montserrat', 18, 'bold'), text_color="#2BC8FF", image=gem_photo, compound="top", command=click_gems, fg_color="transparent", hover_color="#181820", corner_radius=20)
button1.grid(row=0, column=0, padx=15, pady=20)

button2 = ctk.CTkButton(center_frame, text="Farm Money\n$$$", font=('Montserrat', 22, 'bold'), text_color="#00E676", image=money_photo, compound="top", command=click, fg_color="transparent", hover_color="#181820", corner_radius=20)
button2.grid(row=0, column=1, padx=15, pady=20)

button3 = ctk.CTkButton(center_frame, text="Farm Tokens\n🪙🪙🪙", font=('Montserrat', 18, 'bold'), text_color="#FFD700", image=token_photo, compound="top", command=click_tokens, fg_color="transparent", hover_color="#181820", corner_radius=20)
button3.grid(row=0, column=2, padx=15, pady=20)

# STATS & UPGRADES PANEL
bottom_frame = ctk.CTkFrame(window, corner_radius=18, fg_color="#181820", border_width=1, border_color="#2A2A35")
bottom_frame.pack(fill="x", pady=15, padx=30)

upgrade_left = ctk.CTkFrame(bottom_frame, fg_color="transparent")
upgrade_left.pack(side="left", fill="both", expand=True, padx=30, pady=20)

upgrade_right = ctk.CTkFrame(bottom_frame, fg_color="transparent")
upgrade_right.pack(side="right", fill="both", expand=True, padx=30, pady=20)

purchase_button = ctk.CTkButton(upgrade_left, command=purchase_upgrade, text=f"Click Upgrade: ${float(upgrade_cost):.2f}", font=('Montserrat', 15), corner_radius=10, height=35)
purchase_button.pack(pady=4, anchor="w", fill="x")

purchase_button_passive = ctk.CTkButton(upgrade_left, command=purchase_upgrade_passive, text=f"Passive Upgrade: ${float(upgrade_cost_passive):.2f}", font=('Montserrat', 15), corner_radius=10, height=35)
purchase_button_passive.pack(pady=4, anchor="w", fill="x")

gem_upgrade_btn = ctk.CTkButton(upgrade_left, command=purchase_gem_upgrade, text=f"Gem Upgrade (Power x1.0): 💎 {float(gem_upgrade_cost):.1f}", font=('Montserrat', 15, 'bold'), fg_color="#2BC8FF", hover_color="#1DA1CC", text_color="#121212", corner_radius=10, height=35)
gem_upgrade_btn.pack(pady=4, anchor="w", fill="x")

token_upgrade_btn = ctk.CTkButton(upgrade_left, command=purchase_token_upgrade, text=f"Token Upgrade (Passive x1.0): 🪙 {float(token_upgrade_cost):.1f}", font=('Montserrat', 15, 'bold'), fg_color="#FFD700", hover_color="#CCAC00", text_color="#121212", corner_radius=10, height=35)
token_upgrade_btn.pack(pady=4, anchor="w", fill="x")

prestige_button = ctk.CTkButton(upgrade_left, command=purchase_prestige, text=f"Prestige (x1.0): $1000.00", font=('Montserrat', 16, 'bold'), fg_color="#BB86FC", hover_color="#9965D4", text_color="#121212", corner_radius=10, height=40)
prestige_button.pack(pady=(12, 4), anchor="w", fill="x")

current_power = ctk.CTkLabel(upgrade_right, text=f"$ Per Click: ${float(click_power):.3f}", font=('Montserrat', 16), text_color="#B0B0B0")
current_power.pack(pady=4, anchor="e")

money_per_sec = ctk.CTkLabel(upgrade_right, text=f"$ Per Second: ${float(passive_income):.3f}", font=('Montserrat', 16), text_color="#B0B0B0")
money_per_sec.pack(pady=4, anchor="e")

prestige_label = ctk.CTkLabel(upgrade_right, text=f"Prestige Level: {prestige_level}", font=('Montserrat', 17, 'bold'), text_color="#BB86FC")
prestige_label.pack(pady=6, anchor="e")

total_money_label = ctk.CTkLabel(upgrade_right, text=f"Total Earned: ${float(total_money):.3f}", font=('Montserrat', 14), text_color="#606060")
total_money_label.pack(pady=2, anchor="e")

total_gems_label = ctk.CTkLabel(upgrade_right, text=f"Total Gems: 💎 {float(total_gems):.0f}", font=('Montserrat', 14), text_color="#2BC8FF")
total_gems_label.pack(pady=2, anchor="e")

total_tokens_label = ctk.CTkLabel(upgrade_right, text=f"Total Tokens: 🪙 {float(total_tokens):.0f}", font=('Montserrat', 14), text_color="#FFD700")
total_tokens_label.pack(pady=2, anchor="e")

window.geometry(f"{screen_width}x{screen_height}")
try:
    window.state("zoomed")
except:
    pass
window.resizable(True, True)

load_game()
load_ui()

autosave()
money_per_second()
window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()