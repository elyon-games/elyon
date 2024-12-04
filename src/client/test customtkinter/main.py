import customtkinter as ctk


app = ctk.CTk()
app.geometry("700x700")

header = ctk.CTkFrame(master=app, width=700,height=300, fg_color="lightblue")
header.pack(fill="x")

titre = ctk.CTkLabel(header, text="Bienvenu sur Elyon", fg_color="transparent")
titre.grid(row=3)
titre.grid_columnconfigure(0, weight=1)

button_connexion = ctk.CTkButton(header, text="connexion")
button_connexion.grid(row=10)

main_tendance = ctk.CTkFrame(master=app, width=700, fg_color="red")
main_tendance.pack(fill="x")

jeu_tendance=ctk.CTkFrame(master=main_tendance, width=100, height=100)
jeu_tendance.grid(row=0, column=0)

label = ctk.CTkLabel(jeu_tendance, text="Jeu tendance")
label.grid(row=0, column=0)
bouton = ctk.CTkButton(jeu_tendance, text="play")
bouton.grid(row=10, column=0)


main = ctk.CTkFrame(master=app, width=700, fg_color="green")
main.pack(fill="x")
main_content={}

for i in range(1,3+1):
    main_content[f"historique{i}"]=ctk.CTkFrame(master=main, width=100, height=100)
    main_content[f"historique{i}"].grid(row=0, column=i)
    label=ctk.CTkLabel(main_content[f"historique{i}"], text=f"jeu {i}")
    label.grid(row=0, column=0)
    button = ctk.CTkButton(main_content[f"historique{i}"], text="play")
    button.grid(row=10, column=0)

app.mainloop()