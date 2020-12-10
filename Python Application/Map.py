from tkinter import *
from PIL import ImageTk, Image
import pandas as pd
from tkinter.messagebox import showinfo
import os


#initialize main GUI canvas
root = Tk()


def clicked(event):
    print(str(event.x) + " " + str(event.y))


# method goes back to original menu with submit and sliders
def back(self):
    global button
    global w
    #button.place(x=416, y=623)
    w.destroy()

#open excel sheet for ground truth
def open_ground_truth():
    file = "/Users/keeshanpatel/Google Drive/UT/2020 Fall Semester/AI-Design/Project/Code/Austin-Map-master/ground_truth.csv"
    os.system("open -a 'Microsoft Excel.app' '%s'" % file)

#methods to calculate ranks of communities based on slider weights
def get_ranks(slider_list):

    #getting total of slider
    sum_weights = 0
    for slide in slider_list:
        weight = slide[1].get()
        sum_weights += weight
    if sum_weights == 0:
        sum_weights =1

    #getting weight of each factor
    for slide in slider_list:
        weight = slide[1].get()
        weight_factor = weight/sum_weights
        slide[2] = weight_factor

    #calcualting final score based on weights
    neighboorhoods = csv.index.tolist()
    neighboorhood_list = []
    for neigh in neighboorhoods:
        neighboorhood_list.append([neigh,0])

    for i in range (0, len(neighboorhood_list)):
        neighboorhood_name = neighboorhood_list[i][0]
        final_weight = 0

        for slide in slider_list:
            factor_name = slide[0]
            factor_weight = slide[2]
            factor_value = csv.loc[neighboorhood_name, factor_name]
            final_weight += float(factor_value)*factor_weight

        neighboorhood_list[i][1] = final_weight
        print(str(neighboorhood_name) + "\t\t\t\t\t\t" + str(final_weight))

    #sort by final score
    neighboorhood_list = sorted(neighboorhood_list, key=lambda l: l[1], reverse=True)

    print(neighboorhood_list)
    return neighboorhood_list

#For Transperancy to show how the weights were calculated
#shows in pop up window
def get_equation(name):
    print(name + " info button clicked")

    #creates string to show calculated total
    equation_string = str(name) + "\nFactor:Value * Weight = Final Weighting\n"
    total = 0
    for slide in slider_list:
        factor_name = slide[0]
        factor_weight = slide[2]
        factor_value = csv.loc[name, factor_name]
        factor_final_weight = factor_value*factor_weight
        total += factor_final_weight
        if factor_final_weight !=0:
            equation_string += str(factor_name[0:10]) + ": " + str(round(factor_value,2)) + " * " + str(round(factor_weight,2)) + " = " + str(round(factor_final_weight,2)) + "\n"

    #Tallies final score to display
    equation_string += "="*20 + '\n'
    equation_string += "Final Sum Score: " + str(int(round(total)))

    showinfo(name + " Score Breakdown", equation_string)

    return

#After you hit submit this function will run
def display_results():
    global map_img
    global w
    #Create new canvas for map and ranks
    w = Canvas(root, width=100, height=100, bg='white')
    w.pack(expand=YES, fill=BOTH)
    w.create_image((0, 0), image=map_img, anchor=NW)

    # get values of sliders
    for slide in slider_list:
        print("slide: " + str(slide[0]))
        print("slider value: " + str(slide[1].get()))

    # call methods to do calculations
    neighboorhood_list = get_ranks(slider_list)

    #placing ranks on map and printing ranks from greatest to least
    for neighboorhood_index in range (0, len(neighboorhood_list)):
        rank = str(neighboorhood_index+1)
        neighboorhood_name = neighboorhood_list[neighboorhood_index][0]
        neighboorhood_text = rank + "-" + neighboorhood_name + ": " + str(round(neighboorhood_list[neighboorhood_index][1]))
        y_pos_neigh = (neighboorhood_index+2)*17
        neighboorhood_button = w.create_text((731, y_pos_neigh), text= neighboorhood_text, font="Times 10 bold")

        #binds button to nieghboorhood name and places on screen
        button = Button(w,text="info", height = 1, width = 2,command=lambda neighboorhood_name = neighboorhood_name: get_equation(neighboorhood_name))
        button.place(x=830, y=y_pos_neigh-12)

        #places rank on map
        x_coord  = coords.loc[neighboorhood_name, "x_coord"]
        y_coord = coords.loc[neighboorhood_name, "y_coord"]
        w.create_text((x_coord, y_coord), text= rank, font="Times 10 bold")

    w.create_text((731, 15), text="Rank-Name: Score", font="Times 15 bold")

    #create back button
    buttonBG = w.create_rectangle(247, 875, 347, 900, fill="grey60", outline="grey40")
    textButton = w.create_text((297, 887), text='Back')
    w.tag_bind(textButton, "<Button-1>", back)
    w.pack(expand=YES, fill=BOTH)



if "__main__" == __name__:
    #read csv files into pandas dataframe
    csv = pd.read_csv("ground_truth.csv")
    csv.set_index("Neighboorhood", inplace=True)

    #set neighboorhood name as index for rows
    coords = pd.read_csv("Austin_Coords.csv")
    coords.set_index("Neighboorhood", inplace=True)

    #Initialize map of Austin
    root.title('Austin Map')
    root.geometry("894x937")
    map_img = ImageTk.PhotoImage(Image.open("AustinMap.png"))

    # Uncomment out to see where the coordinates of the mouse click are
    #root.bind("<Button 1>", clicked)

    columns = csv.columns
    print(columns)

    slider_list = []

    #create sliders base don input grouth truth columns
    for i in range (0,len(columns)):
        y_pos = (i+1)*40
        slider = Scale(root, from_=0, to=3, orient=HORIZONTAL)
        slider.place(x=400, y=y_pos)
        label = Label(root, text=columns[i], font="Times 12 bold")
        label.place(x=250, y=y_pos+20)
        slider_list.append([columns[i],slider,0])

    #write age preference
    label = Label(root, text="Age Preferences", font="Times 12 bold")
    label.place(x=150, y=60)

    #create submit button
    button = Button(root, text="submit", command=lambda: display_results())
    button.place(x=800, y=914)

    # create source data
    button = Button(root, text="Source Data", command=lambda: open_ground_truth())
    button.place(x=800, y=10)

    c = Canvas(root, width=100, height=100, bg='white')
    label = Label(root, text='Austin Neighborhood Finder', font="Times 20 bold")
    label.place(x=340, y=0)

    root.mainloop()
