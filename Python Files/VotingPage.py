from tkinter import *
from tkinter.ttk import *

import PIL
import mysql.connector
from PIL import ImageTk, Image
from cryptography.fernet import Fernet


def main(paths_list, IDs, voter_id):
    def encrypt(message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)

    def cast_vote():

        try:
            dbConn = mysql.connector.connect(host="127.0.0.1", user="NSuneel", passwd="SqNSun@@sqMuMy3905",
                                             auth_plugin='mysql_native_password', database="electionDB")
            dbCursor = dbConn.cursor()
        except ConnectionError as e:
            print(e)

        vote = int(v.get())
        print(vote)

        voteNameQuery = "select candidateSymbol from candidatemaster where candidateID = " + str(vote)

        dbCursor.execute(voteNameQuery)

        voteChoice = dbCursor.fetchone()[0]
        print(voteChoice)

        privateKey = Fernet.generate_key()

        encVote = encrypt(voteChoice.encode(), privateKey)

        voteQuery = "update votermaster set voterVote = %s where voterID = %s"

        updParams = [str(encVote), voter_id]
        dbCursor.execute(voteQuery, updParams)

        voteQueryPK = "update votermaster set voterPK = %s where voterID = %s"

        updParams = [str(privateKey), voter_id]
        dbCursor.execute(voteQueryPK, updParams)

        dbConn.commit()




    lucida_font = "Lucida Calligraphy"
    heading_font = "Dubai Medium"
    verdana_font = "Verdana"
    georgia_font = "Georgia"
    active_blue_colour = "#03045E"

    root = Toplevel()

    root.geometry("750x650")
    root.title("Casting Vote Window")

    style = Style()
    style.configure('TButton', font=(lucida_font, 10, 'bold', 'underline'),
                    borderwidth='6', activebackground=active_blue_colour,
                    background='cyan')
    style.configure('TRadiobutton', font=(georgia_font, 10))

    images = paths_list
    ids = IDs

    Label(root, text="Casting Your Vote", font=(heading_font, 30)).pack()

    Label(root, text="\nChoose one of the parties from the provided "
                     "list and hit submit...\n",
          font=(verdana_font, 12)).pack()

    new_frame = Frame(root)
    images_list = []
    image_tk = []
    v = StringVar(root)
    Label(root, text="\nCast Your Vote Here\n",
          font=(verdana_font, 18)).pack()

    logo_frame = Frame(root)
    logo_1 = Image.open("data/OtherPhotos/cast_vote.jpg")
    logo = logo_1.resize((300, 150), Image.ANTIALIAS)
    logo_im = ImageTk.PhotoImage(logo)
    Label(logo_frame, image=logo_im).pack()
    logo_frame.pack()

    for path in images:
        images_list.append(Image.open(path).resize((50, 50), Image.ANTIALIAS))
    for ele in images_list:
        image_tk.append(ImageTk.PhotoImage(ele))

    for free in range(len(image_tk)):
        # print(type(image_tk[free]))
        Radiobutton(new_frame, image=image_tk[free], variable=v,
                    value=ids[free]).pack(fill=X, ipady=5)

    new_frame.pack()
    Label(root, text="\n").pack()
    Button(root, text="Submit", command=cast_vote).pack()

    root.mainloop()


if __name__ == '__main__':
    paths = ["data/PartySymbols/bottle.jpg", "data/PartySymbols/chair.jpg",
             "data/PartySymbols/eagle.jpg", "data/PartySymbols/elephant.jpg",
             "data/PartySymbols/door.jpg"]
    ids = ["1", "2", "3", "4", "5"]
    main(paths, ids)
