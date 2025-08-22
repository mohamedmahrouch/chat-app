import socket
import threading
import sqlite3
import json
class ChatServer:
    def __init__(self):
        self.HOST = "127.0.0.1"
        self.PORT = 5555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        self.clients = []
        self.surnoms = []

        self.conn = sqlite3.connect('utilisateurs1.db')
        self.cursor = self.conn.cursor()

        self.create_tables()

        self.shutdown_event = threading.Event()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_nom TEXT,
                receiver_nom TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                nom TEXT PRIMARY KEY,
                password TEXT,
                email TEXT,
                prenom TEXT,
                numero INTEGER,
                genre TEXT
            )
        ''')
        self.conn.commit()

    def broadcast_server_message(self, message, sender_socket):
        for c in self.clients:
            if c != sender_socket:
            
                try:
                    print(f"{message}")
                    c.send(message.encode("utf-8"))
                except:
                    self.remove(c)     

    def remove(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            surnom = self.surnoms[index]

            print("Diffuser le message avant de fermer la connexion")
            self.broadcast_server_message(f"{surnom} a quitté le chat.\n", client)

            print("Retirer le client et le surnom associé")
            self.clients.remove(client)
            self.surnoms.remove(surnom)

            print("Fermer la connexion du client")
            client.close()
         
    def send_surnoms(self, client):
            
      
        
        try:
            
            print("Convertir la liste en chaîne JSON")
            surnoms_json = json.dumps(self.surnoms)
            client.send("votre demande est  succès ".encode('utf-8'))
            client.sendall(surnoms_json.encode('utf-8'))
         
        except Exception as e:
            print(f"Erreur lors de l'envoi des surnoms au client : {e}")

    def handle(self, client):
        while not self.shutdown_event.is_set():
            try:
                message = client.recv(1024).decode("utf-8")
               
                print(f"{message}")
                if message.startswith("CREATE_ACCOUNT"):
                    self.create_account_command(client, message)
                elif message.startswith("SEND_MESSAGE"):
                    
                    self.send_message_command(client, message)
                    print(client)     
                elif message == "REQUEST_HISTORY":
                    
                    self.recuperer_historique_messages(client)    
                elif message.startswith("LOGIN"):
                    self.login_command(client, message)
                if message.startswith("changer le nom"):
                    self.change_name_command(client, message)    
                elif message == "REQUEST_SURNOMS":
                    self.send_surnoms(client) 
                if message == "REQUEST_PROFILE_DATA":
                    self.send_profile_data(client)       
                elif message.startswith("prive"):
                    parts = message.split(";")
                    sender_nom,receiver_nom,prive,receiver_prive,mess = parts[1:] 
                    message=(f"{sender_nom}-->{receiver_prive}:{mess}(prv)")
                    print("message privé :")
                    print(f"{message}")
                    print("recevoir:")
                    print(receiver_prive)
                    print("les clients connectes sont :")
                    print(self.surnoms)
                    if receiver_prive in self.surnoms:
                        index=self.surnoms.index(receiver_prive)
                        print(f"{index}")
                        client=self.clients[index]
                        print(f"{client}")
                        for c in self.clients:
                         if c == client:
                          try:
                           
                            print(f"{message}")
                            c.send(message.encode("utf-8"))
                            
                          except:
                                self.remove(c)   
            
                               
                                print(f"{message}")

                
                elif message == "/serverquit":
                    self.remove(client)
            
            except:
                self.remove(client)
                break
    def change_name_command(self, client, message):
        parts = message.split(";")
        new_name = parts[1]

        
        index = self.clients.index(client)
        old_name = self.surnoms[index]

       
        self.surnoms[index] = new_name

        self.broadcast_server_message(f"{old_name} a changé son nom en {new_name}.\n", client)

       
        self.conn = sqlite3.connect('utilisateurs1.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE utilisateurs SET nom=? WHERE nom=?", (new_name, old_name))
        self.conn.commit()
    def create_account_command(self, client, message):
        message = message.split(";")
        message.remove("CREATE_ACCOUNT")
        nom, password, email, prenom, numero, genre = message

        try:
          
            self.conn = sqlite3.connect('utilisateurs1.db')
            self.cursor = self.conn.cursor()
            print(f"('{nom}','{password}','{email}','{prenom}','{numero}' ,'{genre}')")

            self.cursor.execute(
                f"INSERT INTO utilisateurs VALUES ('{nom}','{password}','{email}','{prenom}','{numero}' ,'{genre}')"
            )

            self.conn.commit()
            client.send("ACCOUNT_CREATED".encode("utf-8"))
        except sqlite3.IntegrityError:
            client.send("ACCOUNT_CREATION_FAILED".encode("utf-8"))
        except Exception as e:
            print(f"Erreur lors de la création du compte : {e}")
            client.send("ACCOUNT_CREATION_FAILED".encode("utf-8"))
        finally:
            self.conn.close()    
    
    def send_message_command(self, client, message):
        parts = message.split(";")
        sender_nom,receiver_nom, content = parts[1:]
      
        print(f"{message}")
        self.broadcast_server_message(f"{sender_nom}-->{receiver_nom}:{content} ",client)
       
        self.conn = sqlite3.connect('utilisateurs1.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('INSERT INTO messages (sender_nom, receiver_nom, content) VALUES (?, ?, ?)',
                        (sender_nom, receiver_nom, content))
        self.conn.commit()
        
      
        
        
    def login_command(self, client, message):
        
        parts = message.split(";")
        nom = parts[1]
        password = parts[2]
        
        if nom and password:
           
           if self.check_account_exists(nom, password):
            client.send("LOGIN_SUCCESS".encode("utf-8"))
            surnom = nom
            self.surnoms.append(surnom)
            self.clients.append(client)
            self.broadcast_server_message(f"{surnom} a rejoint le chat.\n",client)
            var=(f"vous etes connecté !!! ")
            print("var")
            print(f"{var}")
            client.send(var.encode("utf-8"))
           else:
            client.send("LOGIN_FAILED".encode("utf-8"))
        else:
         client.send("LOGIN_FAILED".encode("utf-8"))
    

    def recuperer_historique_messages(self, client):
        self.conn = sqlite3.connect('utilisateurs1.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM messages')
       
        messages = self.cursor.fetchall()
        for message in messages:
            formatted_message = f"{message[1]} -> {message[2]}: {message[3]}\n"
            print(f"{formatted_message}")
            client.send(formatted_message.encode("utf-8"))
        
        
    def check_account_exists(self, nom, password):
        with sqlite3.connect('utilisateurs1.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nom password  FROM utilisateurs WHERE nom=? AND password=?', (nom, password))
            result = cursor.fetchone()
            return result is not None
    def send_profile_data(self, client):
        try:
            print("Entrée dans la fonction send_profile_data")
            user_data = self.get_user_data_from_database(client)
            user_data_json = json.dumps(user_data)
            client.send("Votre demande a réussi".encode('utf-8'))
            client.send(user_data_json.encode('utf-8'))
        except Exception as e:
           
            print(f"Erreur lors de l'envoi des données du profil : {e}")

    def get_user_data_from_database(self, client):
        try:
            index = self.clients.index(client)
            old_name = self.surnoms[index]
            print("Entrée dans la fonction get_user_data_from_database")
            self.conn = sqlite3.connect('utilisateurs1.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT * FROM utilisateurs WHERE nom=?", (old_name,))
            user_data = self.cursor.fetchone()
            self.conn.close()

            if user_data:
                formatted_user_data = {
                    "nom": user_data[0],
                    "password": user_data[1],
                    "email": user_data[2],
                    "prenom": user_data[3],
                    "numero": user_data[4],
                    "genre": user_data[5],
                   
                }
                return formatted_user_data
            else:
                print(f"Aucun utilisateur trouvé avec le nom : {old_name}")
                return None

        except Exception as e:
           
            print(f"Erreur lors de la récupération des données utilisateur : {e}")  

    def recevoir(self):
        while not self.shutdown_event.is_set():
            try:
                client, address = self.server.accept()
                print(f"Connecté avec {str(address)}")
                
               
                client.send("Connecté au serveur\n".encode("utf-8"))
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except socket.error:
                pass  


    def run(self):
        print("Attente de connexions...")
        with self.server:
            thread = threading.Thread(target=self.recevoir)
            thread.start()

            try:
                thread.join()
            except KeyboardInterrupt:
                print("Arrêt du serveur...")
                self.shutdown_event.set()
                for client in self.clients:
                    self.remove(client)

if __name__ == "__main__":
    server = ChatServer()
    server.run()
