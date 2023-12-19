import mysql.connector
import sys
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="cse_lt",
  database="vinsmoke_project"
)

def main():
    #---------Global--------------------#
    def user_all():

      mycursor = mydb.cursor()

      mycursor.execute("SELECT username FROM users")

      myresult = mycursor.fetchall()
      return myresult  
      
    us_all=user_all()  

    data = us_all
    us_list = [item[0] for item in data]

    def clear_screen():
      os.system('cls' if os.name == 'nt' else 'clear')

    def user_add():
      print("|--------------------Signup Page----------------------|")
      print("|-----------------------------------------------------|")
      print("To Signup Please Enter The Following Fields===>")
      user_i=input("User Name--->")
      pwd_i=input("Password--->")
      mycursor = mydb.cursor()
      sql=(f"INSERT INTO users (username,pwd,type) SELECT '{user_i}','{pwd_i}','user' WHERE NOT EXISTS (SELECT 1 FROM users WHERE username='{user_i}')")
      mycursor.execute(sql)
      mydb.commit()
      clear_screen()
      main()
    
    #-----------Starting Page-------------#
    print("|-----------------------------------------------------|")
    print("|------Welcome To Vinsmoke Transport Solutions--------|")
    print("|-----------------------------------------------------|")
    print("1.Login")
    print("2.Signup")
    print("3.Exit")
    op=int(input("Select A Option--->"))
    clear_screen()

    if op==1:
      print("|--------------------Login Page-----------------------|")
      print("|-----------------------------------------------------|")

      user_i=input("User Name--->")
      pwd_i=input("Password--->")
      clear_screen()
    elif op==2:
      user_add()
    elif op==3:
      sys.exit()
    elif op>3 or op<1:
        print("Please Enter Valid Option ID.")   
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        main()
    
    #-------------Defined Functions--------------#

    def user_spec():

       mycursor = mydb.cursor()

       mycursor.execute("SELECT * FROM users where username='"+user_i+"'")
       myresult = mycursor.fetchall()
       if not myresult:
          msg=["Invalid Username.","Invalid Username.","Invalid Username.","Invalid Username."]
          return msg
       else:
          finres=myresult[0]
          return finres

    def pg_admin():
      print("|-------------------Admin Page------------------------|")
      print("1.Add Routes")
      print("2.Exit")
      print("|-----------------------------------------------------|")
      op=int(input("Select A Option--->"))
      clear_screen()
      print("|-----------------------------------------------------|")
      if op==1:
        tick_add()  
      elif op==2:
        sys.exit()
      elif op>2 or op<1:
        print("Please Enter Valid Option ID.")   
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        pg_admin()    

    def pg_2():
      print("|----------------Welcome "+user_i+" ------------------|")
      print("|----------------------Menu---------------------------|")
      print("|-----------------------------------------------------|")
      print("|---------------Signed In As-->"+us_spec[3]+"------------------|")
      print("|-----------------------------------------------------|")

      print("1.Available Routes")
      print("2.My Tickets")
      print("3.Add Review")
      print("4.Exit")
      print("|-----------------------------------------------------|")
      op=int(input("Select A Option--->"))
      clear_screen()
      if op==1:
        avail()
      elif op==2:
        tick_his()
      elif op==3:
        review_add()  
      elif op==4:
        sys.exit() 
      elif op>4 or op<1 :
        print("Please Enter Valid Option ID.")   
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        pg_2()

    def avail():
      print("|------------------Search Tickets------------------|")
      br=input("Enter Boarding Point-->")
      ar=input("Enter Arriving Point-->")
      clear_screen()
      print("|------------------Mode Of Transport------------------|")
      print("1.Bus")
      print("2.Train")
      print("3.Airplanes")
      print("|-----------------------------------------------------|")
      op_m=int(input("Select A Option--->"))
      clear_screen()
      if op_m==1:
         mode="Bus"
      elif op_m==2:
         mode="Train"
      elif op_m==3:
         mode="Airplane"
      elif op_m>3 or op_m<1:
        print("Please Enter Valid Option ID.")   
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        avail()
      try:
        with mydb.cursor() as mycursor:
            sql = "SELECT * FROM cost_mon WHERE mode = %s and av_seats>0 and board LIKE '%"+br+"%' and arrive LIKE '%"+ar+"%' "
            mycursor.execute(sql, (mode,))
            tickets = mycursor.fetchall()

            if not tickets:
                print("No tickets found for the selected category.")
                print("|-----------------------------------------------------|")
                q=input("To Continue Press Any Key...")
                clear_screen()
                pg_2()
            else:
                print("|-------------------Available Tickets-----------------|")
                print(f"Tickets for the selected category ({mode}):")
                for ticket in tickets:
                    print("|-----------------------------------------------------|")
                    print(f"ID: {ticket[3]}")
                    print(f"Company: {ticket[0]}")
                    print(f"Mode: {ticket[1]}")
                    print(f"Boarding DateTime: {ticket[4]}")
                    print(f"Boarding Point: {ticket[5]}")
                    print(f"Arrival Point: {ticket[6]}")
                    print(f"Arrival DateTime: {ticket[7]}")
                    print(f"Cost: {ticket[2]}")
                    print(f"Available Seats: {ticket[8]}")
                print("|-----------------------------------------------------|")
                print("Mention The Id of The Route U Wish To Book Ticket For.")
                op_tick=int(input("-->"))
                is_valid_ticket_number(op_tick,mode)
                clear_screen()
        mydb.commit()
      except mysql.connector.Error as err:
        print(f"Error: {err}")
        q=input("To Continue Press Any Key...")
        clear_screen()
        pg_2()

    def is_valid_ticket_number(ticket_number,mode):
        try:
            ticket_number = int(ticket_number)
            if ticket_number <= 0:
                return False
        except ValueError:
            return False

        try:
           mycursor = mydb.cursor()
           mycursor.execute("SELECT co_id FROM cost_mon WHERE co_id = %s and mode= %s and av_seats>0", (ticket_number,mode,))
           result = mycursor.fetchone()
           if result:
            clear_screen()
            print("|-----------------------------------------------------|")
            print("Succesfull Transaction.")
            mycursor = mydb.cursor()
            sql=("INSERT INTO tick_req (user_i, date, comp, mode, to_cost, board_datetime, board, arrive, arrive_datetime, stat) SELECT '"+user_i+"',CURDATE(),comp,mode,cost,board_datetime,board,arrive,arive_datetime,'Confirmed' FROM cost_mon WHERE co_id="+str(ticket_number))
            mycursor.execute(sql)

            mycursor = mydb.cursor()
            sql_update=("UPDATE cost_mon SET av_seats = av_seats - 1 WHERE co_id = "+str(ticket_number)+" AND mode ='"+mode+"' ")
            mycursor.execute(sql_update)
            mydb.commit()

            tick_view()
           else:
              clear_screen()
              print("Please Enter Valid Route No.")
              print("|-----------------------------------------------------|")
              q=input("To Continue Press Any Key...")
              clear_screen()
              avail()
        except mysql.connector.Error as err:
           print(f"Error: {err}")
           return False
        finally:
            mycursor.close()


    def tick_view():
      mycursor = mydb.cursor()
      mycursor.execute("SELECT * FROM tick_req ORDER BY tick_no DESC LIMIT 1")
      myresult= mycursor.fetchall()
      for i in myresult:
        tick_no=i[10]
        user=i[8]
        date=i[9]
        board=i[0]
        arrive=i[1]
        boardt=i[6]
        arrivet=i[7]
        comp=i[2]
        mode=i[5]
        cost=i[4]
        stat=i[3]
        print("|-----------------------------------------------------|")
        print(f"Ticket No.==>{tick_no}")
        print(f"Date==>{date}")
        print(f"User Id ==>{user}")
        print(f"Company Name ==>{comp}")
        print(f"Mode ==>{mode}")
        print(f"Boarding Point ==>{board}  Boarding Time ==>{boardt}")
        print(f"Arriving Point ==>{arrive}  Boarding Time ==>{arrivet}")
        print(f"Total Cost ==>{cost}")
        print(f"Status Of Ticket ==>{stat}")
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        pg_2()

    def tick_his():
      mycursor = mydb.cursor()
      query = "SELECT * FROM tick_req WHERE user_i = '"+user_i+"' ORDER BY date"
      mycursor.execute(query)
      myresult = mycursor.fetchall()

      print("|-----------------My Tickets---------------------------|")
      for row in myresult:
          tick_no = row[10]
          user = row[8]
          date = row[9]
          board = row[0]
          arrive = row[1]
          boardt = row[6]
          arrivet = row[7]
          comp = row[2]
          mode = row[5]
          cost = row[4]
          stat = row[3]

          print(f"Ticket No.==>{tick_no}  Date==>{date}  User Id ==>{user}  Company Name ==>{comp}  Mode ==>{mode}  Boarding Point ==>{board}  Boarding Time ==>{boardt}  Arriving Point ==>{arrive}  Boarding Time ==>{arrivet}  Total Cost ==>{cost}  Status Of Ticket ==>{stat}")
          print("|-----------------------------------------------------|")
      q=input("To Continue Press Any Key...")
      clear_screen()
      pg_2()

    def tick_add():
      co_id=input("ID==>")
      comp=input("Company==>")
      mode=input("Mode==>")
      board=input("Boarding Point==>")
      boardd=input("Boarding Date==>")
      boardt=input("Boarding Time==>")
      arrive=input("Arriving Point==>")
      arrived=input("Arriving Date==>")
      arrivet=input("Arriving Time==>")
      cost=input("Total Cost==>")
      av_seats=input("Number Of Seats==>")
      clear_screen()
      try:
        with mydb.cursor() as mycursor:
            sql = "INSERT INTO cost_mon (co_id, comp, mode, board_datetime, board, arrive, arive_datetime, cost, av_seats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (co_id, comp, mode, f"{boardd} {boardt}", board, arrive, f"{arrived} {arrivet}", cost, av_seats)
            mycursor.execute(sql, values)
        mydb.commit()
        print("Ticket added successfully!")
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        pg_admin()
      except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("|-----------------------------------------------------|")
        print("Please Enter Valid Values.")
        print("|-----------------------------------------------------|")
        q=input("To Continue Press Any Key...")
        clear_screen()
        tick_add()      

    def review_add():
      add=input("Please Add Ur Review Here===>")
      clear_screen()
      mycursor = mydb.cursor()
      sql=(f"INSERT INTO review_main (user_i,review) values ('{user_i}','{add}')")
      mycursor.execute(sql)
      mydb.commit()
      print("|-----------------------------------------------------|")
      print("Thank You For Sharing Your Thoughts With Us.")
      print("|-----------------------------------------------------|")
      q=input("To Continue Press Any Key...")
      clear_screen()
      pg_2()

   #------------------Code Snippets-----------------#
    us_spec=user_spec()

    if pwd_i==us_spec[2]:
      if "admin"==us_spec[3]:
        pg_admin()
      elif "user"==us_spec[3]:
        pg_2()
    elif pwd_i not in us_spec:
      print("Wrong Credentials.")
      print("|-----------------------------------------------------|")
      q=input("To Continue Press Any Key...")
      clear_screen()
      main()



main()        