import inquirer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("===== Student Performance Analysis Panel! =====")

students = pd.read_csv("Students.csv")
classes = pd.read_csv("Classes.csv")
subjects = pd.read_csv("Subjects.csv")


def ques_df():
    ques_df = [
        inquirer.List("df", message="Select an item:",
                      choices=["Student", "Class", "Subject"])
    ]
    ans_df = inquirer.prompt(ques_df)
    df = ans_df.get("df")
    return df


def ques_method():
    ques_method = [
        inquirer.List(
            "method",
            message="Select a method",
            choices=[
                "Search", "Scroll"
            ])
    ]
    ans_method = inquirer.prompt(ques_method)
    method = ans_method.get("method")

    return method




while True:

    ques_function = [
        inquirer.List("function",
                      message="Choose an operation to perform",
                      choices=['Add', 'Remove', 'Marks',
                               'View', 'Analyze', 'Quit'],
                      ),
    ]
    ans_function = inquirer.prompt(ques_function)
    function = ans_function.get("function")

    student_list = []
    for i in students["Name"]:
        student_list.append(i)

    class_list = []
    for i in classes["Name"]:
        class_list.append(i)

    subject_list = []
    for i in subjects["Name"]:
        subject_list.append(i)

    max_student_id = students["AdminNo"].max()
    max_class_id = classes["Id"].max()
    max_subject_id = subjects["Id"].max()

    ############## ADD Functionality ##############
    if function == "Add":
        print("You have chosen the ADD operation")
        print()
        df = ques_df()

        ############## ADD STUDENT Functionality ##############
        if df == "Student":
            print("You have chosen STUDENT")
            print("Fill out the form to create a new student record.")

            first_name = input("FIRST NAME: ")
            last_name = input("LAST NAME: ")
            age = int(input("AGE: "))

            ques_class = [
                inquirer.List("class", message="Assign a class",
                              choices=class_list)
            ]
            ans_class = inquirer.prompt(ques_class)

            info = {
                "AdminNo": max_student_id+1,
                "Name": first_name + " " + last_name,
                "Age": age,
                "Class": ans_class.get("class")
            }
            students = pd.concat([students, pd.DataFrame([info])])
            for col in subjects["Name"]:
                if f"SUBJECT: {col}" not in students.columns:
                    students[f"SUBJECT: {col}"] = 0
                students[f"SUBJECT: {col}"].fillna(0, inplace=True)
            students.to_csv("Students.csv", index=False)
            print(f"A new student record for {
                  first_name + " " + last_name} has been created!")

        ############## ADD CLASS Functionality ##############
        if df == "Class":
            print("You have chosen CLASS")
            print("Fill out the form to create a new class.")
            while True:
                name = int(
                    input("Enter the class grade (numeric value e.g 11, 12 etc): "))
                if name in class_list:
                    print("Class already exists")
                else:
                    info = {"Id": max_class_id+1, "Name": name}
                    classes = pd.concat([classes, pd.DataFrame([info])])
                    classes.to_csv("Classes.csv", index=False)
                    print(f"Class {name}th has been created!")
                    break

        ############## ADD TEST Functionality ##############
        if df == "Subject":
            print("You have chosen SUBJECT")
            print(
                "Enter a name, total marks & the minimum passing marks.")
            name = input("NAME: ")
            t_marks = int(input("TOTAL MARKS: "))
            m_marks = int(input("MINIMUM PASSING MARKS: "))

            info = {
                "Id": max_subject_id+1,
                "Name": name,
                "Total Marks": t_marks,
                "Passing Marks": m_marks
            }
            subjects = pd.concat([subjects, pd.DataFrame([info])])
            subjects.to_csv("Subjects.csv", index=False)
            students[f"SUBJECT: {name}"] = 0
            students.to_csv("Students.csv", index=False)
            print(
                f"{name} has been generated! The default marks for all students will be set to 0")

    ############## REMOVE Functionality ##############
    if function == "Remove":
        print("You have chosen the REMOVE operation")
        print()
        df = ques_df()

        ############## REMOVE STUDENT Functionality ##############
        if df == "Student":

            print("WARNING: You are going to remove a student from the record!")

            method = ques_method()

            if method == "Scroll":

                select_student_list = [
                    inquirer.List(
                        "student",
                        message="Select a student to remove",
                        choices=student_list
                    )
                ]

                ans = inquirer.prompt(select_student_list)
                selection = ans.get("student")

                students = students[students["Name"] != selection]

                students.to_csv("Students.csv", index=False)
                print(f"{selection} was removed from the list of students!")

            else:
                while True:
                    get_first_name = input("FIRST NAME: ")
                    get_last_name = input("LAST NAME: ")
                    student_name = get_first_name + " " + get_last_name
                    if student_name in student_list:
                        students = students[students["Name"] != student_name]
                        students.to_csv("Students.csv", index=False)
                        print(
                            f"{student_name} was removed from the list of students!")
                        break
                    else:
                        print(
                            "STUDENT NOT FOUND! Please ensure that you are using the correct spellings")

        ############## REMOVE CLASS Functionality ##############
        if df == "Class":
            print(
                "WARNING: You are going to remove a class. All students from that class will also be removed.")

            method = ques_method()

            if method == "Scroll":

                select_class_list = [
                    inquirer.List(
                        "class",
                        message="Select a class to remove",
                        choices=class_list
                    )
                ]

                ans = inquirer.prompt(select_class_list)
                selection = ans.get("class")

                classes = classes[classes["Name"] != selection]
                students = students[students["Class"] != selection]

                classes.to_csv("Classes.csv", index=False)
                students.to_csv("Students.csv", index=False)
                print(f"Class {selection}th was removed.")

            else:
                while True:
                    class_name = int(input("NAME: "))
                    if class_name in class_list:
                        classes = classes[classes["Name"] != class_name]
                        students = students[students["Class"] != class_name]

                        classes.to_csv("Classes.csv", index=False)
                        students.to_csv("Students.csv", index=False)
                        print(f"Class {class_name}th was removed.")
                        break
                    else:
                        print(
                            "CLASS NOT FOUND! Please ensure that you are using the correct spellings")

        ############## REMOVE SUBJECT Functionality ##############
        if df == "Subject":
            print(
                "WARNING: You are going to remove a subject. That column will be deleted from each Student's record")

            method = ques_method()

            if method == "Scroll":

                select_test_list = [
                    inquirer.List(
                        "test",
                        message="Select a class to remove",
                        choices=subject_list
                    )
                ]

                ans = inquirer.prompt(select_test_list)
                selection = ans.get("test")

                subjects = subjects[subjects["Name"] != selection]
                del students[f"SUBJECT: {selection}"]

                subjects.to_csv("Subjects.csv", index=False)
                students.to_csv("Students.csv", index=False)
                print(f"{selection} subject has been deleted.")

            else:
                while True:
                    subject_name = input("NAME: ")
                    if subject_name in subject_list:
                        subjects = subjects[subjects["Name"] != subject_name]
                        del students[f"SUBJECT: {subject_name}"]

                        subjects.to_csv("Subjects.csv", index=False)
                        students.to_csv("Students.csv", index=False)
                        print(f"{subject_name} subject has been deleted.")
                        break
                    else:
                        print(
                            "SUBJECT NOT FOUND! Please ensure that you are using the correct spellings")

    ############## VIEW Functionality ##############
    if function == "View":
        print("You have chosen VIEW operation")
        print()
        df = ques_df()

        if df == "Student":
            print(students.to_string(index=False))
        if df == "Class":
            print(classes.to_string(index=False))
        if df == "Subject":
            print(subjects.to_string(index=False))

     ############## ENTER MARKS Functionality ##############
    if function == "Marks":
        print("You are about to ENTER/UPDATE the marks of a student. ")

        select_student_list = [
            inquirer.List(
                "student",
                message="Select a student to ENTER/UPDATE the marks",
                choices=student_list
            )
        ]

        ans = inquirer.prompt(select_student_list)
        selection = ans.get("student")

        selected_admin_no = students.loc[students["Name"]
                                         == selection, 'AdminNo'].values[0]

        for i in subject_list:
            marks = int(input(f"Enter marks for {i}: "))

            selected_admin_no_list = [selected_admin_no]

            students.loc[students["AdminNo"].isin(
                selected_admin_no_list), f"SUBJECT: {i}"] = marks

            students.to_csv("Students.csv", index=False)

    ############## COMPARE Functionality ##############
    if function == "Analyze":
        print("You have chosen ANALYZE operation")
        print()
        select_student_list = [
            inquirer.List(
                "student",
                message="Select a student",
                choices=student_list
            )
        ]

        ans1 = inquirer.prompt(select_student_list)
        student1 = ans1.get("student")

        select_student2_list = [
            inquirer.List(
                "student",
                message="Select another student",
                choices=student_list
            )
        ]

        ans2 = inquirer.prompt(select_student2_list)
        student2 = ans2.get("student")

        X_axis = np.arange(len(subject_list))

        stu1_marks = []
        stu2_marks = []

        for i in subject_list:
            stu1_marks.append(
                students.loc[students["Name"] == student1, f'SUBJECT: {i}'].values[0])

        for i in subject_list:
            stu2_marks.append(
                students.loc[students["Name"] == student2, f'SUBJECT: {i}'].values[0])

        plt.bar(X_axis - 0.2, stu1_marks, 0.4, label=student1)
        plt.bar(X_axis + 0.2, stu2_marks, 0.4, label=student2)

        plt.xticks(X_axis, subject_list)
        plt.xlabel("Subjects")
        plt.ylabel("Marks")
        plt.title(f"Head-to-Head of {student1} and {student2}")
        plt.legend()
        plt.show()

    ############## QUIT Functionality ##############
    if function == "Quit":
        break
