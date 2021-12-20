from tkinter import *
from tkinter.ttk import *

import PIL
import cv2
import mysql.connector
from PIL import ImageTk
import pandas as pd

import VotingPage
from FaceDetector import detect_face
from ImageSimilarity import image_sim

import time

CURRENT_ELECTION_TYPE = "Parliament"


def main():
    def destroy_win(root_win: Tk):
        for widget in root_win.winfo_children():
            widget.destroy()

    def take_inputs():
        aadhaarName = name.get()
        voterID = int(aadhaar.get())

        try:
            dbConn = mysql.connector.connect(host="127.0.0.1", user="NSuneel", passwd="SqNSun@@sqMuMy3905",
                                             auth_plugin='mysql_native_password', database="electionDB")
            dbCursor = dbConn.cursor()
        except ConnectionError as e:
            print(e)

        dbCursor.execute("select * from votermaster")

        queryResult = dbCursor.fetchall()

        voterMasterCols = [col[0] for col in dbCursor.description]

        resultDF = pd.DataFrame(queryResult)

        aadhaarList = list(resultDF[voterMasterCols.index('voterID')])

        def binary_search(searchList, left, right, ele):
            if right >= left:
                middle = left + (right - left) // 2

                if searchList[middle] == ele:
                    return middle

                elif searchList[middle] > ele:
                    return binary_search(searchList, left, middle - 1, ele)

                elif searchList[middle] < ele:
                    return binary_search(searchList, middle + 1, right, ele)

            else:
                return -1

        voter_id = binary_search(aadhaarList, 0, len(aadhaarList) - 1, voterID) + 1

        constIDQuery = "select * from votermaster where voterID = (%s)"

        voter = [voter_id]

        dbCursor.execute(constIDQuery, voter)

        resQuery = dbCursor.fetchall()

        resDF = pd.DataFrame(resQuery)

        if CURRENT_ELECTION_TYPE == "Parliament":
            constituencyName = resDF[voterMasterCols.index('voterPConstituency')][0]
        else:
            constituencyName = resDF[voterMasterCols.index('voterAConstituency')][0]

        voterPhotoPath = str(resDF[voterMasterCols.index('voterPhoto')][0])

        face_cascade = cv2.CascadeClassifier('face_detection.xml')

        video_capture = cv2.VideoCapture(0)
        width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while True:
            global frame
            ret, frame = video_capture.read()

            faces = face_cascade.detectMultiScale(
                frame,
                scaleFactor=1.1,
                minNeighbors=4
            )

            cv2.circle(frame, (int(width / 2), int(height / 2)), 5, (0, 0, 255), -1)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        voter_photo = detect_face(voterPhotoPath[1:])
        sim_percentage = image_sim(frame, voter_photo)

        cv2.waitKey()

        if sim_percentage > 50 and voter_id > 0:

            constituencyQuery = "select constituencyID from constituencymaster where " \
                                "constituencyName = (%s) and " \
                                "constituencyType = (%s)"

            queryParams = [constituencyName, CURRENT_ELECTION_TYPE]

            dbCursor.execute(constituencyQuery, queryParams)

            queryRes = dbCursor.fetchone()

            constituencyID = queryRes[0]

            candidateQuery = "select * from candidatemaster where canConstituencyID = " + str(constituencyID)

            dbCursor.execute(candidateQuery)

            candidateMasterCols = [col[0] for col in dbCursor.description]

            canQuery = dbCursor.fetchall()

            candidateDF = pd.DataFrame(canQuery)

            candidatesList = [path[1:] for path in list(candidateDF[candidateMasterCols.index('candidateIcon')])]

            candidatesIDList = list(candidateDF[candidateMasterCols.index('candidateID')])

            destroy_win(root)
            success_label = Label(root, text="Verification Successful\nRedirecting To Casting Window",
                                  font=(heading_font, 20)) \
                .place(relx=0.5, rely=0.5, anchor='center')
            time.sleep(2)

            VotingPage.main(candidatesList, candidatesIDList, voter_id)

        else:
            error_label = Label(root, text="Verification Failed", font=(heading_font, 20)) \
                .place(relx=0.5, rely=0.5, anchor='center')
            time.sleep(2)
            destroy_win(root)
            main()

        # loading_label = Label(root, text="Redirecting to casting window", font=(heading_font, 30)) \
        #     .place(relx=0.5, rely=0.5, anchor='center') \
        # time.sleep(5)

    root = Tk()
    window_height = 600
    window_width = 450
    button_width = 100
    selected_fonts = ["Courier New Greek", "Dubai Medium", "Georgia",
                      "Lucida Calligraphy", "Courier New"]
    entry_font = "Courier New"
    heading_font = "Dubai Medium"
    lucida_font = "Lucida Calligraphy"
    heading_font = "Dubai Medium"
    verdana_font = "Verdana"
    georgia_font = "Georgia"
    active_blue_colour = "#03045E"
    georgia_font = "Georgia"
    verdana_font = "Verdana"
    blue_colour = "#00B4D8"
    active_blue_colour = "#03045E"
    red_colour = '#E63946'

    root.title("Login Window")
    name_frame = Frame(root)
    aadhaar_frame = Frame(root)
    button_frame = Frame(root)
    root.geometry(str(window_height) + "x" + str(window_width))

    aadhaar = StringVar()
    name = StringVar()

    style = Style()
    style.configure('TButton', font=(lucida_font, 10, 'bold', 'underline'),
                    borderwidth='6', activebackground=active_blue_colour,
                    background='cyan')
    style.configure('TLabel', font=(verdana_font, 10))
    style.configure('TEntry', font=entry_font)

    heading_label = Label(root, text="Welcome to Home Page", font=(heading_font, 30))

    # bullet_points = Listbox()
    # bullet_points.insert(1, "1. Enter Name and Voter ID")
    # bullet_points.insert(2, "2. Click Verify to perform facial recognition")
    # bullet_points.insert(3, "3. Line face up with center of the red dot")
    # bullet_points.insert(4, "4. Place yourself in a well lit background")
    # bullet_points.insert(5, "5. Position yourself at arm's length from camera")
    # bullet_points.insert(6, "6. Once ready, press 'q' on keyboard to take picture")
    #
    # bullet_points.pack()
    #
    # time.sleep(10)
    # destroy_win(root)

    instruction_label = Label(root, text="\nEnter Name and Aadhaar details\n",
                              font=(verdana_font, 18))
    name_label = Label(name_frame, text="Enter name:", width=15).pack(side=LEFT)
    name_entry = Entry(name_frame, textvariable=name).pack(side=RIGHT)
    aadhaar_label = Label(aadhaar_frame, text="Enter Voter ID:", width=15).pack(side=LEFT, pady=5)
    aadhaar_entry = Entry(aadhaar_frame, textvariable=aadhaar).pack(side=RIGHT, pady=5)

    gap = Label(root, text="\n")

    image1 = PIL.Image.open("data/OtherPhotos/vote_pic.jpg")
    image1 = image1.resize((300, 150), PIL.Image.ANTIALIAS)
    im = ImageTk.PhotoImage(image1)
    # print(type(im))
    Label(root, image=im).pack()

    submit_button = Button(button_frame, text='Verify',
                           command=take_inputs).pack(side=RIGHT, padx=10)

    cancel_button = Button(button_frame, text='Cancel',
                           command=root.destroy).pack(side=LEFT, padx=10)

    heading_label.pack()
    instruction_label.pack()
    name_frame.pack()
    aadhaar_frame.pack()
    gap.pack()
    button_frame.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
