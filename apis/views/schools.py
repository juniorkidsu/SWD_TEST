
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore


class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        # credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
        #                    {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
        #                    {"subject_id": 5, "credit_id": 9}]
        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        score = request.data.get("score", None)
        subject_id = None
        credit_student = None
        for sub_context in subjects_context:
            if sub_context["title"] == subjects_title:
                subject_id = sub_context["id"]
                break
        # Check subject have in condition
        if subject_id == None:
            return Response("No Subject in condition",status=status.HTTP_200_OK,content_type="text/plain; charset=utf-8")
        
        for credit in credits_context:
            if subject_id in credit["subject_id_list_that_using_this_credit"]:
                credit_student = credit["credit"]
                break
        if credit_student == None:
            return Response("No Credit Student in pattern partition",status=status.HTTP_200_OK,content_type="text/plain; charset=utf-8") 

        # Filter Objects Example
        Data = Personnel.objects.filter(first_name=student_first_name, last_name=student_last_name).last()
        find_subject_id = StudentSubjectsScore.objects.filter(student_id=Data.id, subjects_id=subject_id, credit=credit_student).last()
        #Search Subject_id already in Tables>
        if find_subject_id:
            StudentSubjectsScore.objects.filter(student_id=Data.id, subjects_id=subject_id).update(score=score)
            return Response(f"Student : {student_first_name} Score have been Updated",status=status.HTTP_202_ACCEPTED,content_type="text/plain; charset=utf-8") 
        else:
            # Add new Score without exists
            StudentSubjectsScore.objects.create(student_id=Data.id, subjects_id=subject_id, score=score, credit=credit_student)

        return Response(f"Student : {student_first_name} Score have been add in Table",status=status.HTTP_201_CREATED,content_type="text/plain; charset=utf-8") 


class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """

        student_id = kwargs.get("id", None)
        grade_compare = {"A":80,"B+":75,"B":70,"C+":65,"C":60,"D+":55,"D":50}
        example_context_data = {
            "student":{},
            "subject_detail":[],
            "grade_point_average":None
        }
        Data = Personnel.objects.filter(id=student_id).last()
        Student_score = StudentSubjectsScore.objects.filter(student_id=Data.id)
        School_name = Schools.objects.all()
        Count_score = 0
        for data_school in School_name:
            if data_school.id == Data.school_class_id:
                example_context_data["student"] = {
                    'id': Data.id,
                    'full_name': f"{Data.first_name} {Data.last_name}",
                    'school': data_school.title}
        for detail_score in Student_score:
            Score_grade = [k for k,v in grade_compare.items() if int(detail_score.score) <= v and int(detail_score.score)>=v]
            Score_grade = ['F'] if Score_grade == [] else Score_grade 
            Count_score+=detail_score.score
            example_context_data["subject_detail"].append(
                {
                    "subject": detail_score.subjects_id,
                    "credit" : detail_score.credit,
                    "score"  : detail_score.score,
                    "grade"  : Score_grade[0]
                }
            )
        Average_grade = [k for k,v in grade_compare.items() if int(Count_score//4) <=v and int(Count_score//4)>=v]
        Average_grade = ['F'] if Average_grade == [] else Average_grade
        example_context_data["grade_point_average"] = Average_grade[0]
        # example_context_data = {
        #     "student":
        #         {
        #             "id": "primary key of student in database",
        #             "full_name": "student's full name",
        #             "school": "student's school name"
        #         },

        #     "subject_detail": [
        #         {
        #             "subject": "subject's title 1",
        #             "credit": "subject's credit 1",
        #             "score": "subject's score 1",
        #             "grade": "subject's grade 1",
        #         },
        #         {
        #             "subject": "subject's title 2",
        #             "credit": "subject's credit 2",
        #             "score": "subject's score 2",
        #             "grade": "subject's grade 2",
        #         },
        #     ],

        #     "grade_point_average": "grade point average",
        # }

        return Response(example_context_data, status=status.HTTP_200_OK)


class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """

        data_pattern = [
            "1. school: Dorm Palace School, role: Teacher, class: 1,name: Mark Harmon",
            "2. school: Dorm Palace School, role: Teacher, class: 2,name: Jared Sanchez",
            "3. school: Dorm Palace School, role: Teacher, class: 3,name: Cheyenne Woodard",
            "4. school: Dorm Palace School, role: Teacher, class: 4,name: Roger Carter",
            "5. school: Dorm Palace School, role: Teacher, class: 5,name: Cynthia Mclaughlin",
            "6. school: Dorm Palace School, role: Head of the room, class: 1,name: Margaret Graves",
            "7. school: Dorm Palace School, role: Head of the room, class: 2,name: Darren Wyatt",
            "8. school: Dorm Palace School, role: Head of the room, class: 3,name: Carla Elliott",
            "9. school: Dorm Palace School, role: Head of the room, class: 4,name: Brittany Mullins",
            "10. school: Dorm Palace School, role: Head of the room, class: 5,name: Nathan Solis",
            "11. school: Dorm Palace School, role: Student, class: 1,name: Aaron Marquez",
            "12. school: Dorm Palace School, role: Student, class: 1,name: Benjamin Collins",
            "13. school: Dorm Palace School, role: Student, class: 1,name: Carolyn Reynolds",
            "14. school: Dorm Palace School, role: Student, class: 1,name: Christopher Austin",
            "15. school: Dorm Palace School, role: Student, class: 1,name: Deborah Mcdonald",
            "16. school: Dorm Palace School, role: Student, class: 1,name: Jessica Burgess",
            "17. school: Dorm Palace School, role: Student, class: 1,name: Jonathan Oneill",
            "18. school: Dorm Palace School, role: Student, class: 1,name: Katrina Davis",
            "19. school: Dorm Palace School, role: Student, class: 1,name: Kristen Robinson",
            "20. school: Dorm Palace School, role: Student, class: 1,name: Lindsay Haas",
            "21. school: Dorm Palace School, role: Student, class: 2,name: Abigail Beck",
            "22. school: Dorm Palace School, role: Student, class: 2,name: Andrew Williams",
            "23. school: Dorm Palace School, role: Student, class: 2,name: Ashley Berg",
            "24. school: Dorm Palace School, role: Student, class: 2,name: Elizabeth Anderson",
            "25. school: Dorm Palace School, role: Student, class: 2,name: Frank Mccormick",
            "26. school: Dorm Palace School, role: Student, class: 2,name: Jason Leon",
            "27. school: Dorm Palace School, role: Student, class: 2,name: Jessica Fowler",
            "28. school: Dorm Palace School, role: Student, class: 2,name: John Smith",
            "29. school: Dorm Palace School, role: Student, class: 2,name: Nicholas Smith",
            "30. school: Dorm Palace School, role: Student, class: 2,name: Scott Mckee",
            "31. school: Dorm Palace School, role: Student, class: 3,name: Abigail Smith",
            "32. school: Dorm Palace School, role: Student, class: 3,name: Cassandra Martinez",
            "33. school: Dorm Palace School, role: Student, class: 3,name: Elizabeth Anderson",
            "34. school: Dorm Palace School, role: Student, class: 3,name: John Scott",
            "35. school: Dorm Palace School, role: Student, class: 3,name: Kathryn Williams",
            "36. school: Dorm Palace School, role: Student, class: 3,name: Mary Miller",
            "37. school: Dorm Palace School, role: Student, class: 3,name: Ronald Mccullough",
            "38. school: Dorm Palace School, role: Student, class: 3,name: Sandra Davidson",
            "39. school: Dorm Palace School, role: Student, class: 3,name: Scott Martin",
            "40. school: Dorm Palace School, role: Student, class: 3,name: Victoria Jacobs",
            "41. school: Dorm Palace School, role: Student, class: 4,name: Carol Williams",
            "42. school: Dorm Palace School, role: Student, class: 4,name: Cassandra Huff",
            "43. school: Dorm Palace School, role: Student, class: 4,name: Deborah Harrison",
            "44. school: Dorm Palace School, role: Student, class: 4,name: Denise Young",
            "45. school: Dorm Palace School, role: Student, class: 4,name: Jennifer Pace",
            "46. school: Dorm Palace School, role: Student, class: 4,name: Joe Andrews",
            "47. school: Dorm Palace School, role: Student, class: 4,name: Michael Kelly",
            "48. school: Dorm Palace School, role: Student, class: 4,name: Monica Padilla",
            "49. school: Dorm Palace School, role: Student, class: 4,name: Tiffany Roman",
            "50. school: Dorm Palace School, role: Student, class: 4,name: Wendy Maxwell",
            "51. school: Dorm Palace School, role: Student, class: 5,name: Adam Smith",
            "52. school: Dorm Palace School, role: Student, class: 5,name: Angela Christian",
            "53. school: Dorm Palace School, role: Student, class: 5,name: Cody Edwards",
            "54. school: Dorm Palace School, role: Student, class: 5,name: Jacob Palmer",
            "55. school: Dorm Palace School, role: Student, class: 5,name: James Gonzalez",
            "56. school: Dorm Palace School, role: Student, class: 5,name: Justin Kaufman",
            "57. school: Dorm Palace School, role: Student, class: 5,name: Katrina Reid",
            "58. school: Dorm Palace School, role: Student, class: 5,name: Melissa Butler",
            "59. school: Dorm Palace School, role: Student, class: 5,name: Pamela Sutton",
            "60. school: Dorm Palace School, role: Student, class: 5,name: Sarah Murphy"
        ]
        school_title = kwargs.get("school_title", None)
        role_name = {"0":"Teacher","1":"Head of the room","2":"Student"}
        school_map = {"1":"Rose Garden School","2":"Dorm Palace School","3":"Prepare Udom School"}
        id_school = [k for k,v in school_map.items() if v == school_title]
        if id_school == []:
            return Response(f"No School Title to check in Database",status=status.HTTP_201_CREATED,content_type="text/plain; charset=utf-8") 
        Class_data = Classes.objects.filter(school_id=id_school[0])
        class_detail = []
        your_result = []
        for classes in Class_data:
            class_detail.append(int(classes.class_order))
        All_Data_in_school_name = Personnel.objects.filter(school_class_id__in=class_detail).order_by('personnel_type','school_class_id')
        for i in All_Data_in_school_name:
            role = [v for k,v in role_name.items() if i.personnel_type == int(k)]
            your_result.append(f"{i.id} school: {school_title}, role: {role[0]}, class: {i.school_class_id}, name: {i.first_name} {i.last_name}")

        return Response(your_result, status=status.HTTP_200_OK)


class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "school": "Dorm Palace School",
                "class 1": {
                    "Teacher: Mark Harmon": [
                        {
                            "Head of the room": "Margaret Graves"
                        },
                        {
                            "Student": "Aaron Marquez"
                        },
                        {
                            "Student": "Benjamin Collins"
                        },
                        {
                            "Student": "Carolyn Reynolds"
                        },
                        {
                            "Student": "Christopher Austin"
                        },
                        {
                            "Student": "Deborah Mcdonald"
                        },
                        {
                            "Student": "Jessica Burgess"
                        },
                        {
                            "Student": "Jonathan Oneill"
                        },
                        {
                            "Student": "Katrina Davis"
                        },
                        {
                            "Student": "Kristen Robinson"
                        },
                        {
                            "Student": "Lindsay Haas"
                        }
                    ]
                },
                "class 2": {
                    "Teacher: Jared Sanchez": [
                        {
                            "Head of the room": "Darren Wyatt"
                        },
                        {
                            "Student": "Abigail Beck"
                        },
                        {
                            "Student": "Andrew Williams"
                        },
                        {
                            "Student": "Ashley Berg"
                        },
                        {
                            "Student": "Elizabeth Anderson"
                        },
                        {
                            "Student": "Frank Mccormick"
                        },
                        {
                            "Student": "Jason Leon"
                        },
                        {
                            "Student": "Jessica Fowler"
                        },
                        {
                            "Student": "John Smith"
                        },
                        {
                            "Student": "Nicholas Smith"
                        },
                        {
                            "Student": "Scott Mckee"
                        }
                    ]
                }
            }
        ]
        collect_data = {}
        mapping_school = []
        mapping_class_school = []
        School_hold_id = 0
        new_class_school = False
        new_class = False
        Before_school = ""
        your_result = []
        All_school = Schools.objects.all()
        for i in All_school:
            mapping_school.append(f"{i.id}:{i.title}")
        All_class = Classes.objects.all()
        # ------------- MAPPING CLASS WITH SCHOOL ID ---------------------------- #

        for j in All_class:
            for map in mapping_school:
                id_type = map.split(":")[0]
                School_name = map.split(":")[-1]
                if id_type == str(j.school_id):
                    mapping_class_school.append(f"{j.id}|{j.class_order}|{School_name}")

        # ------------- MAPPING CLASS WITH SCHOOL ID ---------------------------- #
        All_Data_Personal = Personnel.objects.all().order_by('school_class_id')
        for data_student in All_Data_Personal:
            school_class_id = data_student.school_class_id
            get_school_every_loop = [i.split("|")[-1] for i in mapping_class_school if i.split("|")[0] == str(school_class_id)]
            if School_hold_id != school_class_id:
                new_class = True
            for detail_school in mapping_class_school:
                if str(data_student.school_class_id) == detail_school.split("|")[0] and Before_school != get_school_every_loop[0]:
                    if collect_data != {}:
                        your_result.append(collect_data)
                        collect_data = {}
                    collect_data["school"] = detail_school.split("|")[2]
                    Before_school = detail_school.split("|")[2]
                if str(data_student.school_class_id) == detail_school.split("|")[0] and new_class == True:
                    class_at = detail_school.split("|")[1]
                    collect_data[f"class {class_at}"] = {}
                    new_class = False
            if data_student.personnel_type == 0:
                collect_data[f"class {class_at}"][f"Teacher: {data_student.first_name} {data_student.last_name}"] = []
                Teacher_name = f"Teacher: {data_student.first_name} {data_student.last_name}"
                School_hold_id = data_student.school_class_id
            if data_student.personnel_type == 1:
                collect_data[f"class {class_at}"][f"{Teacher_name}"].append(f"Head of the room : {data_student.first_name} {data_student.last_name}")
            if data_student.personnel_type == 2:
                collect_data[f"class {class_at}"][f"{Teacher_name}"].append(f"Student : {data_student.first_name} {data_student.last_name}")



        your_result.append(collect_data)

        return Response(your_result, status=status.HTTP_200_OK)


class SchoolStructureAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "title": "มัธยมต้น",
                "sub": [
                    {
                        "title": "ม.1",
                        "sub": [
                            {
                                "title": "ห้อง 1/1"
                            },
                            {
                                "title": "ห้อง 1/2"
                            },
                            {
                                "title": "ห้อง 1/3"
                            },
                            {
                                "title": "ห้อง 1/4"
                            },
                            {
                                "title": "ห้อง 1/5"
                            },
                            {
                                "title": "ห้อง 1/6"
                            },
                            {
                                "title": "ห้อง 1/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.2",
                        "sub": [
                            {
                                "title": "ห้อง 2/1"
                            },
                            {
                                "title": "ห้อง 2/2"
                            },
                            {
                                "title": "ห้อง 2/3"
                            },
                            {
                                "title": "ห้อง 2/4"
                            },
                            {
                                "title": "ห้อง 2/5"
                            },
                            {
                                "title": "ห้อง 2/6"
                            },
                            {
                                "title": "ห้อง 2/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.3",
                        "sub": [
                            {
                                "title": "ห้อง 3/1"
                            },
                            {
                                "title": "ห้อง 3/2"
                            },
                            {
                                "title": "ห้อง 3/3"
                            },
                            {
                                "title": "ห้อง 3/4"
                            },
                            {
                                "title": "ห้อง 3/5"
                            },
                            {
                                "title": "ห้อง 3/6"
                            },
                            {
                                "title": "ห้อง 3/7"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "มัธยมปลาย",
                "sub": [
                    {
                        "title": "ม.4",
                        "sub": [
                            {
                                "title": "ห้อง 4/1"
                            },
                            {
                                "title": "ห้อง 4/2"
                            },
                            {
                                "title": "ห้อง 4/3"
                            },
                            {
                                "title": "ห้อง 4/4"
                            },
                            {
                                "title": "ห้อง 4/5"
                            },
                            {
                                "title": "ห้อง 4/6"
                            },
                            {
                                "title": "ห้อง 4/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.5",
                        "sub": [
                            {
                                "title": "ห้อง 5/1"
                            },
                            {
                                "title": "ห้อง 5/2"
                            },
                            {
                                "title": "ห้อง 5/3"
                            },
                            {
                                "title": "ห้อง 5/4"
                            },
                            {
                                "title": "ห้อง 5/5"
                            },
                            {
                                "title": "ห้อง 5/6"
                            },
                            {
                                "title": "ห้อง 5/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.6",
                        "sub": [
                            {
                                "title": "ห้อง 6/1"
                            },
                            {
                                "title": "ห้อง 6/2"
                            },
                            {
                                "title": "ห้อง 6/3"
                            },
                            {
                                "title": "ห้อง 6/4"
                            },
                            {
                                "title": "ห้อง 6/5"
                            },
                            {
                                "title": "ห้อง 6/6"
                            },
                            {
                                "title": "ห้อง 6/7"
                            }
                        ]
                    }
                ]
            }
        ]

        your_result = []
        room_structure = {}
        start_position = 0
        create_new_sub = True
        insert_old_value = False
        Structure = SchoolStructure.objects.all()
        for i in Structure:
            if i.parent_id == None:
                if room_structure != {}:
                    your_result.append(room_structure)
                    room_structure= {}
                    create_new_sub = True
                room_structure["title"]=i.title
                Top_current_room = i.title
                Top_tree = i.id
                insert_old_value = True

            else:
                if i.parent_id == Top_tree:
                    if create_new_sub == True:
                        room_structure["sub"] = []
                        create_new_sub = False
                    # if room_structure["sub"] != []:
                    #     room_structure["sub"].append({"title":i.title})
                    room_structure["sub"].append({"title":i.title})
                    current_len = len(room_structure["sub"])
                    room_structure["sub"][current_len-1]["sub"] = []
                    Top_current_tier2_room = i.title
                    Top_tier2_tree = i.id
                elif i.parent_id == Top_tier2_tree:
                    room_structure["sub"][current_len-1]["sub"].append({"title":i.title})
                

        your_result.append(room_structure)
        return Response(your_result, status=status.HTTP_200_OK)
