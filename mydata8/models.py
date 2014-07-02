from django.db import models
from django.contrib.auth.models import User

# table format source data
from djangotailoring.models import SubjectData

# Create your models here.

# python ../manage.py makemtsmodel > MODEL.OUT (results go below here)

INT_ATTENDANCE_CHOICES = (
    ('0', 'Never'),
    ('1', '1 to 5 times'),
    ('2', '5 to 10 times'),
    ('3', '10 or more times'),
    ('4', "I don't plan on attending lecture"),
)

INT_SLC_CHOICES = (
    ('1', 'Yes'),
    ('0', 'No'),
    ('2', "What's an SLC study group?"),
)

TEXT_APCOURSE_CHOICES = (
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('Physics', 'Physics'),
    ('Math', 'Calculus/Statistics'),
    ('Other', 'Other AP/IB Course'),
)

INT_DISCUSSIONATTENDANCE_CHOICES = (
    ('0', 'Never'),
    ('1', '1 to 2 times'),
    ('2', '3 to 5 times'),
    ('3', 'More than 5 times'),
)

CTEXT_COLLEGE_CHOICES = (
    ('LSA', 'LSA'),
    ('Engineering', 'Engineering'),
    ('Kinesiology', 'Kinesiology'),
    ('Other', 'Other'),
)

INT_YESNO_CHOICES = (
    ('1', 'Yes'),
    ('0', 'No'),
)

PREEXAM2_ANSWERS_CHOICES = (
    ('0', u'I think I\u2019m good to go. I\u2019m comfortable with the material so far.'),
    ('1', u'I\u2019m fine on the math, but some of the other material is really confusing!'),
    ('2', u'Orbitals, VSEPR, I get it. But I\u2019m still having trouble with the calculations!'),
    ('3', u'I\u2019m stuck on a few different things, both math and concepts.'),
)

INT_CONFIDENCERANGE_CHOICES = (
    ('0', 'Not at all confident<br>0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', 'Extremely Confident<br>10'),
)

OPT_OUT_CHOICES = (
    ('0', 'Opt in'),
    ('1', 'Opt out'),
)

CTEXT_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

INT_LOGINFREQUENCY_CHOICES = (
    ('4', 'Multiple times per day'),
    ('3', 'Every day'),
    ('2', 'Once or twice weekly'),
    ('1', 'Almost never'),
)

CINT_SEMSESTERS_COMPLETED_CHOICES = (
    ('9', 'More than 8 semesters'),
)

CTEXT_COLLEGE_CONCENTRATE_CHOICES = (
    ('Engineering', 'Engineering'),
    ('Physics', 'Physics/Astrophysics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('Biology_MCDB', 'Biology MCDB'),
    ('Biology_EEB', 'Biology EEB'),
    ('Health', 'Health-related Field (Physical Therapy, Pharmacology, Nursing, etc.)'),
    ('Humanities', 'Humanities'),
    ('Math', 'Mathematics'),
    ('Stats', 'Statistics'),
    ('Neurosci', 'Neuroscience'),
    ('Social_Science_not_Psych', 'Social Science (excluding Psychology)'),
    ('Psych_BBCS', 'Psychology or BBCS'),
    ('Education', 'Education'),
    ('IDK', 'I do not know'),
    ('Other', 'Other'),
)

CTEXT_POST_COLLEGE_CHOICES = (
    ('Employment', 'Employment'),
    ('Med_School', 'Medical School or other Health-related Professional School'),
    ('Dent_School', 'Dental School'),
    ('Education', 'Education (teaching, policy, or a certification program)'),
    ('Grad_Life_Sci', 'Graduate School in a Life Science discipline'),
    ('Grad_Other', 'Graduate School in another discipline'),
    ('IDK', "Unsure/I don't know"),
    ('Other', 'Other'),
)

INT_AGREEDISAGREE_CHOICES = (
    ('1', 'Agree'),
    ('0', 'Disagree'),
)

INT_INTERESTRANGE_CHOICES = (
    ('0', 'Not at all interested<br>0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', 'Extremely interested<br>10'),
)

CINT_GPA_CHOICES = (
    ('20', '2.0 or lower'),
    ('21', '2.1'),
    ('22', '2.2'),
    ('23', '2.3'),
    ('24', '2.4'),
    ('25', '2.5'),
    ('26', '2.6'),
    ('27', '2.7'),
    ('28', '2.8'),
    ('29', '2.9'),
    ('30', '3.0'),
    ('31', '3.1'),
    ('32', '3.2'),
    ('33', '3.3'),
    ('34', '3.4'),
    ('35', '3.5'),
    ('36', '3.6'),
    ('37', '3.7'),
    ('38', '3.8'),
    ('39', '3.9'),
    ('40', '4.0'),
)

CTEXT_EMPLOYMENT_STATUS_CHOICES = (
    ('No_Job', 'I do not have a job'),
    ('Part_Time', 'I work a part-time job (20 hours or less a week)'),
    ('Full_Time', 'I work a full-time job (more than 20 hours a week)'),
)

CTEXT_YES_NO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

CTEXT_INVOLVED_IN_CHOICES = (
    ('Greek', 'Greek Life (Sororities/Fraternities)'),
    ('Sports', 'Sports/Club Sports'),
    ('Religious', 'Religious Organizations'),
    ('Research', 'Research (Thesis, UROP, Lab work)'),
    ('Volunteering', 'Volunteering'),
    ('Music_Art', 'Music/Art'),
    ('Other', 'Other Student Clubs/Organzations'),
)

TEXT_CHEMREASON_CHOICES = (
    ('Possible_Concentrate_req', 'I am considering chemisrty as my concentration'),
    ('Concentration_req', 'Chemistry is required by my concentration'),
    ('Grad_req', 'I need this class to prepare for my graduate/professional program'),
    ('Credit', 'For a specific credit (NS, QR, etc.)'),
    ('Interest', "I'm taking this class because of my interest in chemistry"),
)

TEXT_GTD_CHOICES = (
    ('done', '-'),
)

INT_HOURSSTUDY_CHOICES = (
    ('21', 'More than 20'),
)

CTEXT_CLASS_STANDING_CHOICES = (
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
)

INT_YCLASS_CHOICES = (
    ('1', 'Strongly Disagree<br>1'),
    ('2', '<br>2'),
    ('3', '<br>3'),
    ('4', '<br>4'),
    ('5', 'Strongly Agree<br>5'),
)

INT_TODO_CHOICES = (
    ('0', 'Not Done'),
    ('1', 'Done'),
)

PRE_EXAM_CONFIDENCE_CHOICES = (
    ('0', "I'm feeling great! The material comes naturally to me, and I'm getting through the homeworks without too much trouble."),
    ('1', "I'm feeling okay. Most things are clear to me, but there are one or two topics I know I need to work on."),
    ('2', "I'm a little behind. There are topics that seem too complicated to me, and I feel like I'm struggling a little through the practice resources."),
    ('3', "I'm in panic mode! The course material is overwhelming and I could really use some extra help."),
    ('4', "CHEM 130 has been on my back burner and I haven't really looked at things that much."),
)

POSTEXAM2_FEELS_ANSWERS_CHOICES = (
    ('1', 'Exam 2 was easier because there was less math/more qualitative understanding questions.'),
    ('2', 'I felt more prepared for Exam 2 because I changed my study habits after Exam 1.'),
    ('3', 'I felt worse about Exam 2 because I was expecting more math questions.'),
    ('4', 'The Exam 2 material was new to me, which made the exam more difficult.'),
    ('5', 'I changed my study habits after Exam 1 but I still did worse on Exam 2!'),
    ('6', 'I had a hard time seeing how the Exam 2 material was relevant in the big picture.'),
)

INT_GRADE_DISTRIBUTION_CHOICES = (
    ('8', 'A'),
    ('7', 'A-'),
    ('6', 'B+'),
    ('5', 'B'),
    ('4', 'B-'),
    ('3', 'C+'),
    ('2', 'C'),
    ('1', 'C-'),
    ('0', 'D+ or lower'),
)

CINT_BDAY_MONTH_CHOICES = (
    ('-1', 'Month'),
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

CTEXT_PARENT_ED_CHOICES = (
    ('Less_HS', 'Less than High School'),
    ('HS', 'High School/GED'),
    ('Some_College', 'Some College'),
    ('2_Year_College', '2-Year College Degree (Associates)'),
    ('4_Year_College', '4-Year College Degree (BA, BS)'),
    ('Masters', "Master's Degree"),
    ('Doctoral', 'Doctoral Degree'),
    ('Professional', 'Professional Degree (MD, JD)'),
)


class Source1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_source1'
    ExitQ1_AttribQuote = models.IntegerField(null=True, blank=True)
    ExitQ2_PhotoPermit = models.IntegerField(null=True, blank=True)
    ExitQ3_ClassReDo = models.TextField(null=True, blank=True)
    ExitQ4_ExamPrep = models.TextField(null=True, blank=True)
    ExitQ5_GroupStudy = models.TextField(null=True, blank=True)
    ExitQ6_ExpectedGrade = models.IntegerField(null=True, blank=True)
    ExitQ7_EcoachFrequency = models.IntegerField(null=True, blank=True)
    ExitQ8_PrimaryUse = models.TextField(null=True, blank=True)
    ExitQ9_GoodBadFeatures = models.TextField(null=True, blank=True)
    ExitQ10_Misc = models.TextField(null=True, blank=True)
    Exit_Q11_SurveyTimes = models.TextField(null=True, blank=True)
    Post_Exam2_Feelings__1 = models.NullBooleanField()
    Post_Exam2_Feelings__2 = models.NullBooleanField()
    Post_Exam2_Feelings__3 = models.NullBooleanField()
    Post_Exam2_Feelings__4 = models.NullBooleanField()
    Post_Exam2_Feelings__5 = models.NullBooleanField()
    Post_Exam2_Feelings__6 = models.NullBooleanField()
    Exam_1_Satisfaction = models.IntegerField(null=True, blank=True)
    Exam_2_Satisfaction = models.IntegerField(null=True, blank=True)
    PR_ProblemsTried_Exam2 = models.IntegerField(null=True, blank=True)
    PR_ProblemsTried_Exam1 = models.IntegerField(null=True, blank=True)
    Message_3_Q1 = models.IntegerField(null=True, blank=True)
    Reg_Enrolled = models.IntegerField(null=True, blank=True)
    Reg_GPA = models.FloatField(null=True, blank=True)
    Reg_Gender = models.CharField(max_length=5, null=True, blank=True)
    Reg_Acad_Level = models.CharField(max_length=20, null=True, blank=True)
    Signup_Opt_Out = models.IntegerField(null=True, blank=True)
    ChemPrevious = models.IntegerField(null=True, blank=True)
    Math_Confidence = models.IntegerField(null=True, blank=True)
    YClass09 = models.IntegerField(null=True, blank=True)
    CHEM130HoursStudy = models.IntegerField(null=True, blank=True)
    CHEM130OWLHours = models.IntegerField(null=True, blank=True)
    Mat_Textbook = models.IntegerField(null=True, blank=True)
    Mat_iClicker = models.IntegerField(null=True, blank=True)
    Mat_Calculator = models.IntegerField(null=True, blank=True)
    Exam_1_Score = models.IntegerField(null=True, blank=True)
    Exam_2_Score = models.IntegerField(null=True, blank=True)
    Final_Exam_Score = models.IntegerField(null=True, blank=True)
    CHEM130Friends = models.IntegerField(null=True, blank=True)
    APCourses = models.IntegerField(null=True, blank=True)
    APCoursesTaken__Chemistry = models.NullBooleanField()
    APCoursesTaken__Biology = models.NullBooleanField()
    APCoursesTaken__Physics = models.NullBooleanField()
    APCoursesTaken__Math = models.NullBooleanField()
    APCoursesTaken__Other = models.NullBooleanField()
    CHEM130SLC = models.IntegerField(null=True, blank=True)
    CHEM130Attendance = models.IntegerField(null=True, blank=True)
    CHEM130DiscussionAttendance = models.IntegerField(null=True, blank=True)
    CHEM130GoalGrade = models.IntegerField(null=True, blank=True)
    YClass26 = models.IntegerField(null=True, blank=True)
    YClass27 = models.IntegerField(null=True, blank=True)
    YClass28 = models.IntegerField(null=True, blank=True)
    YClass29 = models.IntegerField(null=True, blank=True)
    YClass30 = models.IntegerField(null=True, blank=True)
    YClass31 = models.IntegerField(null=True, blank=True)
    YClass38 = models.IntegerField(null=True, blank=True)
    YClass39 = models.IntegerField(null=True, blank=True)
    YClass40 = models.IntegerField(null=True, blank=True)
    YClass42 = models.IntegerField(null=True, blank=True)
    YClass43 = models.IntegerField(null=True, blank=True)
    YClass44 = models.IntegerField(null=True, blank=True)
    YClass45 = models.IntegerField(null=True, blank=True)
    YClass48 = models.IntegerField(null=True, blank=True)
    YClass47 = models.IntegerField(null=True, blank=True)
    YClass49 = models.IntegerField(null=True, blank=True)
    YClass50 = models.IntegerField(null=True, blank=True)
    YClass46 = models.IntegerField(null=True, blank=True)
    GTD_01__done = models.NullBooleanField()
    GTD_02__done = models.NullBooleanField()
    GTD_03__done = models.NullBooleanField()
    GTD_04__done = models.NullBooleanField()
    GTD_05__done = models.NullBooleanField()
    GTD_06__done = models.NullBooleanField()
    GTD_07__done = models.NullBooleanField()
    GTD_08__done = models.NullBooleanField()
    GTD_09__done = models.NullBooleanField()
    GTD_10__done = models.NullBooleanField()
    GTD_11__done = models.NullBooleanField()
    GTD_12__done = models.NullBooleanField()
    GTD_13__done = models.NullBooleanField()
    GTD_14__done = models.NullBooleanField()
    GTD_15__done = models.NullBooleanField()
    YClass41 = models.IntegerField(null=True, blank=True)
    YClass32 = models.IntegerField(null=True, blank=True)
    YClass33 = models.IntegerField(null=True, blank=True)
    YClass34 = models.IntegerField(null=True, blank=True)
    YClass35 = models.IntegerField(null=True, blank=True)
    YClass36 = models.IntegerField(null=True, blank=True)
    YClass37 = models.IntegerField(null=True, blank=True)
    YClass10 = models.IntegerField(null=True, blank=True)
    YClass11 = models.IntegerField(null=True, blank=True)
    YClass12 = models.IntegerField(null=True, blank=True)
    YClass18 = models.IntegerField(null=True, blank=True)
    YClass19 = models.IntegerField(null=True, blank=True)
    YClass20 = models.IntegerField(null=True, blank=True)
    YClass21 = models.IntegerField(null=True, blank=True)
    YClass22 = models.IntegerField(null=True, blank=True)
    YClass23 = models.IntegerField(null=True, blank=True)
    YClass24 = models.IntegerField(null=True, blank=True)
    YClass25 = models.IntegerField(null=True, blank=True)
    YClass13 = models.IntegerField(null=True, blank=True)
    YClass14 = models.IntegerField(null=True, blank=True)
    YClass15 = models.IntegerField(null=True, blank=True)
    YClass16 = models.IntegerField(null=True, blank=True)
    YClass17 = models.IntegerField(null=True, blank=True)
    YClass01 = models.IntegerField(null=True, blank=True)
    YClass03 = models.IntegerField(null=True, blank=True)
    YClass02 = models.IntegerField(null=True, blank=True)
    YClass04 = models.IntegerField(null=True, blank=True)
    YClass05 = models.IntegerField(null=True, blank=True)
    YClass06 = models.IntegerField(null=True, blank=True)
    YClass07 = models.IntegerField(null=True, blank=True)
    YClass08 = models.IntegerField(null=True, blank=True)
    CHEM130Reason__Possible_Concentrate_req = models.NullBooleanField()
    CHEM130Reason__Concentration_req = models.NullBooleanField()
    CHEM130Reason__Grad_req = models.NullBooleanField()
    CHEM130Reason__Credit = models.NullBooleanField()
    CHEM130Reason__Interest = models.NullBooleanField()
    CHEM130Confidence = models.IntegerField(null=True, blank=True)
    CHEM130GradeConfidence = models.IntegerField(null=True, blank=True)
    dist_ID = models.TextField(null=True, blank=True)
    CHEM130Interest = models.IntegerField(null=True, blank=True)
    Message_2_Q1 = models.IntegerField(null=True, blank=True)
    Message_2_Q2 = models.IntegerField(null=True, blank=True)
    Message_2_Q3 = models.IntegerField(null=True, blank=True)
    Quiz_Avg_Exam1 = models.FloatField(null=True, blank=True)
    Quiz_Avg_Exam2 = models.FloatField(null=True, blank=True)
    Quiz_Avg_Final = models.FloatField(null=True, blank=True)
    Participation_Avg_Exam1 = models.FloatField(null=True, blank=True)
    Participation_Avg_Exam2 = models.FloatField(null=True, blank=True)
    Participation_Avg_Final = models.FloatField(null=True, blank=True)
    OWL_Avg_Exam1 = models.FloatField(null=True, blank=True)
    OWL_Avg_Exam2 = models.FloatField(null=True, blank=True)
    OWL_Avg_Final = models.FloatField(null=True, blank=True)
    zombi_group = models.IntegerField(null=True, blank=True)
    zombi_1_write = models.TextField(null=True, blank=True)
    zombi_2_write = models.TextField(null=True, blank=True)
    zombi_2_review = models.TextField(null=True, blank=True)
    zombi_3_write = models.TextField(null=True, blank=True)
    zombi_3_review = models.TextField(null=True, blank=True)
    zombi_3_rewrite = models.TextField(null=True, blank=True)
    zombi_4_rewrite = models.TextField(null=True, blank=True)
    PreExam2_Q1 = models.IntegerField(null=True, blank=True)

class EmptySource(SubjectData):
    pass

class Common1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_common1'
    First_Name = models.CharField(max_length=20, null=True, blank=True)
    Last_Name = models.CharField(max_length=20, null=True, blank=True)
    uniqname = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=1, choices=CTEXT_GENDER_CHOICES, null=True, blank=True)
    BirthDay = models.IntegerField(null=True, blank=True)
    BirthMo = models.IntegerField(null=True, blank=True)
    BirthYr = models.IntegerField(null=True, blank=True)
    Semesters_Completed = models.IntegerField(null=True, blank=True)
    College = models.CharField(max_length=11, choices=CTEXT_COLLEGE_CHOICES, null=True, blank=True)
    College_Other = models.CharField(max_length=30, null=True, blank=True)
    Concentrate__Engineering = models.NullBooleanField()
    Concentrate__Physics = models.NullBooleanField()
    Concentrate__Chemistry = models.NullBooleanField()
    Concentrate__Biology = models.NullBooleanField()
    Concentrate__Biology_MCDB = models.NullBooleanField()
    Concentrate__Biology_EEB = models.NullBooleanField()
    Concentrate__Health = models.NullBooleanField()
    Concentrate__Humanities = models.NullBooleanField()
    Concentrate__Math = models.NullBooleanField()
    Concentrate__Stats = models.NullBooleanField()
    Concentrate__Neurosci = models.NullBooleanField()
    Concentrate__Social_Science_not_Psych = models.NullBooleanField()
    Concentrate__Psych_BBCS = models.NullBooleanField()
    Concentrate__Education = models.NullBooleanField()
    Concentrate__IDK = models.NullBooleanField()
    Concentrate__Other = models.NullBooleanField()
    Concentrate_Other = models.CharField(max_length=30, null=True, blank=True)
    Declared = models.CharField(max_length=3, choices=CTEXT_YES_NO_CHOICES, null=True, blank=True)
    Class_Standing = models.CharField(max_length=9, choices=CTEXT_CLASS_STANDING_CHOICES, null=True, blank=True)
    Cum_GPA_Survey = models.IntegerField(null=True, blank=True)
    Employment = models.CharField(max_length=9, choices=CTEXT_EMPLOYMENT_STATUS_CHOICES, null=True, blank=True)
    Involved_In__Greek = models.NullBooleanField()
    Involved_In__Sports = models.NullBooleanField()
    Involved_In__Religious = models.NullBooleanField()
    Involved_In__Research = models.NullBooleanField()
    Involved_In__Volunteering = models.NullBooleanField()
    Involved_In__Music_Art = models.NullBooleanField()
    Involved_In__Other = models.NullBooleanField()
    Other_Commitment = models.CharField(max_length=30, null=True, blank=True)
    Post_College = models.CharField(max_length=13, choices=CTEXT_POST_COLLEGE_CHOICES, null=True, blank=True)
    Parent_Ed = models.CharField(max_length=14, choices=CTEXT_PARENT_ED_CHOICES, null=True, blank=True)
    High_School_CumGPA = models.IntegerField(null=True, blank=True)


