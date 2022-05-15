#!/usr/bin/env python
#
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys
import subprocess
import os
import string
import sys
import time
import datetime
# import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()
# db = MySQLdb.connect("localhost" , "root" , "password")


def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("My first window!")

    label = QLabel(win)
    label.setText("my first label")
    label.move(50, 50)

    win.show()
    sys.exit(app.exec_())


main()  # make sure to call the function


cmd = 'sudo digitemp_DS9097U  -a  -c /home/pi/Desktop/BMS/digitemp1.conf'
timefmt = '%Y-%m-%d %H:%M:%S'
mig = 0
zm_zapis = 0
minuty = 0
akt_minuty = 0

while True:
    # print "START"
    time.sleep(35)
    minuty = time.strftime('%M')
    # print minuty
    if pifacedigital.switches[0].value == 0:
        pfio.digital_write(0, 1)
        # print "Auto"

    else:
        pfio.digital_write(0, 0)
        # print "Manual"

    if mig == 0:
        pfio.digital_write(7, 1)
        mig = 1
    else:
        pfio.digital_write(7, 0)
        mig = 0
    # print time.strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the database
    try:
        db = MySQLdb.Connect(host='localhost', user='root',
                             passwd='reflik', db='pi_base')
    except DatabaseError:
        print("Problem connecting to database")
        sys.exit(-1)

    cursor = db.cursor()
    # odczyt z bazy wartosci zadanej
    polecenie_sql = 'SELECT * FROM w_zadana'
    try:
        cursor.execute(polecenie_sql)
        db.commit()
    except:
        db.rollback()
    rekordy = cursor.fetchall()

    # w_zmienna do R
    # salon
    R1 = rekordy[3][2]
    # print rekordy [3][1],R1
    # lazienka prter
    R2 = rekordy[1][2]
    # print rekordy [1][1],R2
    # gabinet
    R3 = rekordy[0][2]
    # print rekordy [0][1],R3
    # kuchnie
    R4 = rekordy[4][2]
    # print rekordy [4][1],R4
    # lazienka pietro
    R5 = rekordy[5][2]
    # print rekordy [5][1],R5

    # akt_minuty=time.strftime('%M')
    # print akt_minuty
    # if minuty<>akt_minuty:

    for outline in os.popen(cmd).readlines():
        S = string.split(outline, " ")
        G = S[3]

        # print minuty
        if G == "Sensor":

            # print S
            #print (S[0], S[1], S[3], S[4],S[5], S[6])
            my_date = datetime.datetime.fromtimestamp(
                float(S[0])).strftime('%Y-%m-%d %H:%M:%S')
            # print my_date
            mydate = datetime.datetime.fromtimestamp(
                float(S[0])).strftime('%Y-%m-%d')
            # print mydate
            mytime = datetime.datetime.fromtimestamp(
                float(S[0])).strftime('%H:%M:%S')
            # print mytime
            # print S[0]

            try:
                # Execute the SQL command
                cursor.execute("""
                INSERT INTO pomiary2 (my_epoch, date, time, nr_hex, temp, nr_czujnika)
                VALUES
                (%s,%s,%s,%s,%s,%s)
                """, (int(S[0]), mydate, mytime, S[1], S[6], S[4]))

                # Commit your changes in the database
                db.commit()
                print("zapis ", time.strftime('%Y-%m-%d %H:%M:%S'))

            except:
                # Rollback in# case there is any error
                db.rollback()
            # zapis minuty zapisu w bazie do zmiennej minuty

            # kawalek - porownanie zadanej z aktualna

            # pierwsza wartosc zadana
            if S[4] == "22":  # salon 0x28 0x53 0xe9 0xfa 0x01 0x00 0x00 0x81
                X = round(float(S[6]))
                X1 = int(X)
                # print rekordy [3][2]
                # R1=int(R[6])
                #R1=int(rekordy [3][2])
                # print S
                # print R1
                # print X1
                if R1 > X1:  # jesli R > to znaczy ze zadana jest wieksza /
                    # niz aktualna wiec ON
                    # print "ON0"
                    wy0 = 1
                    pfio.digital_write(2, 1)
                else:
                    # print "OFF0"
                    wy0 = 0
                    pfio.digital_write(2, 0)
                try:
                  # Execute the SQL command
                    cursor.execute("""
                  INSERT INTO wyjscie (my_date, my_time, nr_wy, stan)
                  VALUES
                  (%s,%s,%s,%s)
                  """, (mydate, mytime, S[4], wy0))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in# case there is any error
                    db.rollback()

            # druga wartosc zadana
            if S[4] == "19":  # lazienka parter 0x28 0x55 0xfa 0xfa 0x01 0x00 0x00 0x01
                X = round(float(S[6]))
                X1 = int(X)
                # print rekordy [1][2]
                # R2=int(R[2])
                # print S
                # print R2
                # print X1
                if R2 > X1:  # jesli R > to znaczy ze zadana jest wieksza /
                    # niz aktualna wiec ON
                    # print "ON1"
                    wy1 = 1
                    pfio.digital_write(3, 1)
                else:
                    # print "OFF1"
                    wy1 = 0
                    pfio.digital_write(3, 0)
                try:
                    # Execute the SQL command
                    cursor.execute("""
                    INSERT INTO wyjscie (my_date, my_time, nr_wy, stan)
                    VALUES
                    (%s,%s,%s,%s)
                    """, (mydate, mytime, S[4], wy1))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in# case there is any error
                    db.rollback()

            # trzecia wartosc zadana
            if S[4] == "25":  # gabinet 0x28 0x87 0x4b 0xe1 0x03 0x00 0x00 0xca
                X = round(float(S[6]))
                X1 = int(X)
                # print rekordy [0][2]
                # R3=int(R[0])
                # print S
                # print R3
                # print X1
                if R3 > X1:  # jesli R > to znaczy ze zadana jest wieksza /
                    # niz aktualna wiec ON
                    # print "ON1"
                    wy2 = 1
                    pfio.digital_write(4, 1)
                else:
                    # print "OFF1"
                    wy2 = 0
                    pfio.digital_write(4, 0)
                try:
                    # Execute the SQL command
                    cursor.execute("""
                    INSERT INTO wyjscie (my_date, my_time, nr_wy, stan)
                    VALUES
                    (%s,%s,%s,%s)
                    """, (mydate, mytime, S[4], wy2))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in# case there is any error
                    db.rollback()

            # czwarta wartosc zadana
            if S[4] == "27":  # kuchnia 0x28 0x67 0xd2 0xfa 0x01 0x00 0x00 0x44
                X = round(float(S[6]))
                X1 = int(X)
                # print rekordy [4][2]
                # R4=int(R[8])
                # print S
                # print R4
                # print X1
                if R4 > X1:  # jesli R > to znaczy ze zadana jest wieksza /
                    # niz aktualna wiec ON
                    # print "ON1"
                    wy3 = 1
                    pfio.digital_write(5, 1)
                else:
                    # print "OFF1"
                    wy3 = 0
                    pfio.digital_write(5, 0)
                try:
                    # Execute the SQL command
                    cursor.execute("""
                    INSERT INTO wyjscie (my_date, my_time, nr_wy, stan)
                    VALUES
                    (%s,%s,%s,%s)
                    """, (mydate, mytime, S[4], wy3))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in# case there is any error
                    db.rollback()

            # piata wartosc zadana
            if S[4] == "12":  # lazienka pietro 0x28 0x76 0xe8 0xc4 0x01 0x00 0x00 0x4c
                X = round(float(S[6]))
                X1 = int(X)
                # print rekordy [5][2]
                # R5=int(R[10])
                # print S
                # print R5
                # print X1
                if R5 > X1:  # jesli R > to znaczy ze zadana jest wieksza /
                    # niz aktualna wiec ON
                    # print "ON1"
                    wy4 = 1
                    pfio.digital_write(6, 1)
                else:
                    # print "OFF1"
                    wy4 = 0
                    pfio.digital_write(6, 0)
                try:
                    # Execute the SQL command
                    cursor.execute("""
                    INSERT INTO wyjscie (my_date, my_time, nr_wy, stan)
                    VALUES
                    (%s,%s,%s,%s)
                    """, (mydate, mytime, S[4], wy4))
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in# case there is any error
                    db.rollback()

        # disconnect from server
    db.close()  # poza if
    zapis_OK = 1
