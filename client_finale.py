import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import json
from functools import partial
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.surnom = None
        self.email = None
        self.nom = None
        self.gui_donne = False
        self.running = True
        self.email_entry = None
        self.fenetres = []
        self.fenetre = None

    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.surnom = self.receive_message()
    def on_window_close(self, window):
        window.withdraw()     
    def receive_message(self):
        try:
            return self.sock.recv(1024).decode("utf-8")
            
        except ConnectionAbortedError:
            print("La connexion a été fermée par l'autre extrémité.")
            self.stop()  
            exit(1) 

    def send_message(self, message):
        if isinstance(message, str):
         message = message.encode("utf-8")
         self.sock.send(message)
    def show_login_gui(self):
        login_window = tk.Tk()
        login_window.title('Connexion')
        image = Image.open("C:\\Users\\Utilisateur\\Desktop\\projet app chat\\images.png")
        image = image.resize((250, 250))  
        photo = ImageTk.PhotoImage(image)
        #self.fenetre.iconbitmap("C:\\Users\\Utilisateur\\Desktop\\1.ico")
        image_label = tk.Label(login_window, image=photo, bg="#ecf0f1")
        image_label.grid(row=1, rowspan=5, column=0, padx=10, sticky=tk.W)

        nom_label = tk.Label(login_window, text="Nom:", bg="#bdc3c7", fg="#2c3e50")
        nom_label.grid(row=1, column=1, pady=5, padx=20, sticky=tk.W)

        self.nom_entry =tk. Entry(login_window)
        self.nom_entry.grid(row=1, column=2, pady=5, padx=20)

        password_label = tk.Label(login_window, text="Mot de passe:", bg="#bdc3c7", fg="#2c3e50")
        password_label.grid(row=2, column=1, pady=5, padx=20, sticky=tk.W)

        self.password_entry =tk. Entry(login_window, show="*")
        self.password_entry.grid(row=2, column=2, pady=5, padx=20)

        login_btn = tk.Button(login_window, text="Se connecter", command=self.login, bg="#16a085", fg="white")
        login_btn.grid(row=3, column=1, columnspan=2, pady=10)

        create_account_btn = tk.Button(login_window, text="Créer un compte", command=self.show_create_account_gui, bg="#e74c3c", fg="white")
        create_account_btn.grid(row=4, column=1, columnspan=2, pady=10)

        quit_btn = tk.Button(login_window, text="Quitter", command=login_window.destroy, bg="#34495e", fg="white")
        quit_btn.grid(row=5, column=1, columnspan=2, pady=10)
        
        login_window.protocol("WM_DELETE_WINDOW", partial(self.on_window_close, login_window))
        login_window.deiconify()
        self.login_window = login_window 
        
        login_window.mainloop() 

        

    def show_create_account_gui(self):
        create_account_window = tk.Tk()
        create_account_window.title('Créer un compte')

        nom_label = tk.Label(create_account_window, text="Nom:")
        nom_label.grid(row=1, column=0, pady=5, padx=20, sticky=tk.W)

        self.nom_entry_create = tk.Entry(create_account_window)
        self.nom_entry_create.grid(row=1, column=1, pady=5, padx=20)

        password_label = tk.Label(create_account_window, text="Mot de passe:")
        password_label.grid(row=2, column=0, pady=5, padx=20, sticky=tk.W)

        self.password_entry_create = tk.Entry(create_account_window, show="*")
        self.password_entry_create.grid(row=2, column=1, pady=5, padx=20)

        emaillabel = tk.Label(create_account_window, text="email:")
        emaillabel.grid(row=3, column=0, pady=5, padx=20, sticky=tk.W)

        self.email_entry_create = tk.Entry(create_account_window)
        self.email_entry_create.grid(row=3, column=1, pady=5, padx=20)

        prenom_label = tk.Label(create_account_window, text="Prénom:")
        prenom_label.grid(row=4, column=0, pady=5, padx=20, sticky=tk.W)

        self.prenom_entry_create = tk.Entry(create_account_window)
        self.prenom_entry_create.grid(row=4, column=1, pady=5, padx=20)

        numero_label = tk.Label(create_account_window, text="numéro de téléphone:")
        numero_label.grid(row=5, column=0, pady=5, padx=20, sticky=tk.W)

        self.numero_entry_create = tk.Entry(create_account_window)
        self.numero_entry_create.grid(row=5, column=1, pady=5, padx=20)

        genre_label = tk.Label(create_account_window, text="Genre:")
        genre_label.grid(row=6, column=0, pady=5, padx=20, sticky=tk.W)

        self.genre_entry_create = tk.Entry(create_account_window)
        self.genre_entry_create.grid(row=6, column=1, pady=5, padx=20)

        create_btn = tk.Button(create_account_window, text="enregistrer", command=self.create_account, bg="#3498db", fg="white")
        create_btn.grid(row=7, column=0, columnspan=2, pady=10)

        quit_btn = tk.Button(create_account_window, text="Quitter", command=create_account_window.destroy, bg="#34495e", fg="white")
        quit_btn.grid(row=8, column=0, columnspan=2, pady=10)
        create_account_window.protocol("WM_DELETE_WINDOW", partial(self.on_window_close, create_account_window))
        create_account_window.deiconify()
        self.create_account_window = create_account_window
        create_account_window.mainloop()

    def login(self):
        nom = self.nom_entry.get()
        password=self.password_entry.get()
        self.send_message(f"LOGIN;{nom};{password}")
        print(f"{nom}\n")
        print(password)
        response = self.receive_message()
        print(response)
        if response == "LOGIN_SUCCESS":
            self.email =nom
            self.nom = nom
            self.login_window.destroy()
            self.show_chat_gui()
            self.running = True
        else:
            messagebox.showerror("Erreur", "Votre compte n'existe pas ou les informations sont incorrectes.")

    def create_account(self):
      nom = self.nom_entry_create.get()
      password = self.password_entry_create.get()
      email= self.email_entry_create.get()
      prenom = self.prenom_entry_create.get()
      age = self.numero_entry_create.get()
      genre = self.genre_entry_create.get()
      
      if nom and password and email and prenom and age and genre:
        self.send_message(f"CREATE_ACCOUNT;{nom};{password};{email};{prenom};{age};{genre}")
      else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return
      response = self.receive_message()
      print(response) 
      if response == "ACCOUNT_CREATED":
        messagebox.showinfo("Succès", "Compte créé avec succès.")
        self.create_account_window.destroy()
      elif response == "ACCOUNT_CREATION_FAILED":
        messagebox.showerror("Erreur", "le compte deja existe")
      else:
        messagebox.showerror("Erreur", "Réponse inattendue du serveur lors de la création du compte.")

    
    def show_chat_gui(self):
        self.fenetre = tk.Tk()
        self.fenetre.title('Chat client')
        chat_label = tk.Label(self.fenetre, text="BIENVENUE AU CHAT MESSAGING", bg="#3498db", fg="white")
        chat_label.configure(font="arial 12 bold")
        chat_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.text_area = ScrolledText(self.fenetre, bg="#ecf0f1", fg="#2c3e50", wrap=tk.WORD)
        self.text_area.config(state="disabled")
        self.text_area.grid(row=1, column=0, columnspan=2, pady=5)

        msg_label = tk.Label(self.fenetre, text="Message:", bg="#3498db", fg="white")
        msg_label.configure(font="arial 12 bold")
        msg_label.grid(row=2, column=0, pady=5, padx=20, sticky=tk.W)

        saisit = tk.Text(self.fenetre, height=3, bg="#bdc3c7", fg="#2c3e50")
        saisit.grid(row=2, column=1, pady=5, padx=20)

        btn_envoie = tk.Button(self.fenetre, text="Envoyer", command=lambda: self.ecrire(saisit), bg="#2ecc71", fg="white")
        btn_envoie.configure(font="arial 12 bold")
        btn_envoie.grid(row=3, column=0, columnspan=2, pady=5)
         
         
        profile_btn = tk.Button(self.fenetre, text="Profil", command=self.show_profile_gui, bg="#3498db", fg="white")
        profile_btn.grid(row=0, column=1, columnspan=2, pady=12, sticky=tk.E)

        quit_btn = tk.Button(self.fenetre, text="Quitter", command=self.stop, bg="#34495e", fg="white")
        quit_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.gui_donne = True
        self.fenetre.protocol("WM_DELETE_WINDOW", self.stop)
        threading.Thread(target=self.recevoir).start()
        comptes_btn = tk.Button(self.fenetre, text="Comptes en ligne", command=self.afficher_comptes_connectes, bg="#3498db", fg="white")
        comptes_btn.grid(row=4, column=0, columnspan=2, pady=10)

        chat_prive_btn = tk.Button(self.fenetre, text="Chat Privé", command=self.chat_prive, bg="#3498db", fg="white")
        chat_prive_btn.grid(row=5, column=0, columnspan=2, pady=10)

        historique_btn = tk.Button(self.fenetre, text="cliquer pour voir Historique", command=self.afficher_historique_gui, bg="#e74c3c", fg="white")

        historique_btn.grid(row=4, column=0, pady=10, padx=20, sticky=tk.W)

        quit_btn = tk.Button(self.fenetre, text="Quitter", command=self.stop, bg="#34495e", fg="white")
        quit_btn.grid(row=4, column=1, pady=10, padx=20, sticky=tk.E)
        
        modify_name_btn = tk.Button(self.fenetre, text="Modifier le Nom", command=self.modify_name, bg="#3498db", fg="white")
        modify_name_btn.grid(row=0, column=0, pady=10, padx=20, sticky=tk.W)
        self.fenetre.mainloop()
      
    def afficher_comptes_connectes(self):
        self.send_message("REQUEST_SURNOMS")
        comptes_window = tk.Tk()
        comptes_window.title('Comptes Connectés')

        comptes_label = tk.Label(comptes_window, text="Comptes Connectés", bg="#3498db", fg="white")
        comptes_label.configure(font="arial 12 bold")
        comptes_label.grid(row=0, column=0, columnspan=2, pady=5)

        comptes_text = ScrolledText(comptes_window, bg="#ecf0f1", fg="#2c3e50")
        comptes_text.config(state="normal")
        connected_users =self.fetch_connected_users()
        for user in connected_users:
            comptes_text.insert("end", f"{user}\n")

        comptes_text.config(state="disabled")
        comptes_text.grid(row=1, column=0, columnspan=2, pady=5)

        quit_btn = tk.Button(comptes_window, text="Quitter", command=comptes_window.destroy, bg="#34495e", fg="white")
        quit_btn.grid(row=2, column=0, columnspan=2, pady=10)

        comptes_window.mainloop()
           
    def commencer_chat_prive(self, user):
        if user:
            self.selection_window .destroy()
            message = askstring("Message privé", f"Entrez votre message privé pour {user}:")
            if message is not None:
                messagebox.showinfo("Chat Privé", f"Message privé envoyé à {user}: {message}")
                if message:
                        prive="hhhh"
                        mess= message
                        print("ha contenu de message mfere9")
                        print(f"{mess}")
                        message = f"{self.nom};tous;{prive};{user};{mess}"
                        print(f"Message à envoyer : {message}")
                        self.send_message(f"prive;{message}")
                        print("message prive a envoye.")     
            else:
                messagebox.showinfo("Annulation", "Annulation de l'envoi du message privé.")
        else:
             messagebox.showinfo("Erreur", "Veuillez sélectionner un utilisateur.")
         
    def fetch_connected_users(self):
        try:
            print("Recevoir la chaîne JSON directement sans la taille")
            surnoms_json = self.receive_message()

            print(f"{surnoms_json}")
            surnoms = json.loads(surnoms_json)

            return surnoms
        except Exception as e:
            print(f"Erreur lors de la réception des surnoms : {e}")
            return []
    def modify_name(self):
        new_name = askstring("Modifier le Nom", "Entrez votre nouveau nom:")
        if new_name is not None:
            if new_name.strip() != "":
                message = f"changer le nom;{new_name}"
                self.send_message(message)
            else:
                messagebox.showerror("Erreur", "Le nouveau nom ne peut pas être vide.")  
                  
    def chat_prive(self):
        self.send_message("REQUEST_SURNOMS")
        selection_window = tk.Tk()
        selection_window.title('Sélectionner un Utilisateur')

        selection_label = tk.Label(selection_window, text="Sélectionner un Utilisateur", bg="#3498db", fg="white")
        selection_label.configure(font="arial 12 bold")
        selection_label.grid(row=0, column=0, columnspan=2, pady=5)
       
        selection_listbox = tk.Listbox(selection_window, selectmode=tk.SINGLE, bg="#ecf0f1", fg="#2c3e50")
        connected_users =self.fetch_connected_users()
        
        print(f"{connected_users}")
        for user in connected_users:
            selection_listbox.insert(tk.END, user)

        selection_listbox.grid(row=1, column=0, columnspan=2, pady=5)

        chat_btn = tk.Button(selection_window, text="Commencer le Chat Privé", command=lambda: self.commencer_chat_prive(selection_listbox.get(tk.ACTIVE)), bg="#3498db", fg="white")
        chat_btn.grid(row=2, column=0, columnspan=2, pady=10)

        quit_btn = tk.Button(selection_window, text="Quitter", command=selection_window.destroy, bg="#34495e", fg="white")
        quit_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        selection_window.protocol("WM_DELETE_WINDOW", partial(self.on_window_close, selection_window))
        selection_window.deiconify()
        self.selection_window= selection_window 
        selection_window.mainloop() 
            
    def afficher_historique_gui(self):
            self.send_message("REQUEST_HISTORY")
            data = self.sock.recv(4096)
            messages = data.decode("utf-8").split('\n')
            for message in messages:
                if message:
                    parts = message.split('->')
                    sender = parts[0].strip()
                    receiver = parts[1].strip()
                    content = parts[2].strip()
                    self.text_area.insert("end", f"{sender} -> {receiver}: {content}\n")
                     
    def ecrire(self, saisie):
        message_content = saisie.get('1.0', 'end-1c').strip()
        print(f"Le contenu du message est : {message_content}")
        if message_content:
                if message_content.startswith("priveto"):
                    print("Chat privé détecté :")
                    parts = message_content.split(";")
                    prive, receiver_prive, mess = parts[:]
                    print("ha contenu de message mfere9")
                    print(f"{prive}:{receiver_prive}:{mess}")
                    message = f"{self.nom};tous;{prive};{receiver_prive};{mess}"
                    print(f"Message à envoyer : {message}")
                    self.send_message(f"prive;{message}")
                    print("message prive a envoye.")
                    self.text_area.config(state="normal")
                    self.text_area.insert("end", message + "\n")
                    self.text_area.yview("end")
                    self.text_area.config(state="disabled")
                    saisie.delete('1.0', 'end')
                else:
                    message = f"{self.nom};tous;{message_content}"
                    self.send_message(f"SEND_MESSAGE;{message}")
                    print("le message est :")
                    print(f"{message}")
                    parts = message.split(";")
                    print("message a divisé")
                    sender_nom,receiver_nom, content = parts[:]
                    print("t9ssem")
                    message=(f"{"vous"}-->{receiver_nom}:{content} ")
                    print(f"{message}")
                    self.text_area.config(state="normal")
                    self.text_area.insert("end", message + "\n")
                    self.text_area.yview("end")
                    self.text_area.config(state="disabled")
                    saisie.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.fenetre.destroy()
        self.send_message("/serverquit".encode("utf-8"))
        self.sock.close()
        exit(0)

    def recevoir(self):
        while self.running:
            try:
                message = self.receive_message()
               
                print(f"{message}")
                if message:
                    self.text_area.config(state="normal")
                    self.text_area.insert("end", message + "\n")
                    self.text_area.yview("end")
                    self.text_area.config(state="disabled")
            except Exception as e:
                print("Erreur:", str(e))
                self.sock.close()
                break
            
    def show_profile_gui(self):
        self.send_message("REQUEST_PROFILE_DATA")
        profile_data = self.receive_message()  # Assurez-vous que receive_message est défini
        profile_window = tk.Toplevel(self.fenetre)
        profile_window.title("Profil")

        try:
            if profile_data is not None:
                profile_info = json.loads(profile_data)
                for key, value in profile_info.items():
                    label = tk.Label(profile_window, text=f"{key}: {value}\n")
                    label.pack()
            else:
                raise json.JSONDecodeError("profile_data is None", "", 0)

        except json.JSONDecodeError as e:
           
            print(f"Erreur de décodage JSON : {e}")
            error_label = tk.Label(profile_window, text="Erreur de traitement des données du profil.")
            error_label.pack()

        close_button = tk.Button(profile_window, text="Fermer", command=profile_window.destroy)
        close_button.pack()
        self.fenetres.append(profile_window)
client = Client("127.0.0.1", 5555)
client.connect_to_server()
client.show_login_gui()
