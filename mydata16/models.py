from django.db import models
from django.contrib.auth.models import User

# table format source data
from djangotailoring.models import SubjectData

# Create your models here.

# python ../manage.py makemtsmodel > MODEL.OUT (results go below here)

TEXT_PARENTED_CHOICES = (
    ('Less_HS', 'Less than High School'),
    ('HS', 'High School/GED'),
    ('Some_College', 'Some College'),
    ('2_Year_College', '2-Year College Degree (Associates)'),
    ('4_Year_College', '4-Year College Degree (BA, BS)'),
    ('Masters', "Master's Degree"),
    ('Doctoral', 'Doctoral Degree'),
    ('Professional', 'Professional Degree (MD, JD)'),
)

INT_HIGHSCHOOLGPA_CHOICES = (
    ('2_0', 'Less than 2.0'),
    ('2_1', '2.1'),
    ('2_2', '2.2'),
    ('2_3', '2.3'),
    ('2_4', '2.4'),
    ('2_5', '2.5'),
    ('2_6', '2.6'),
    ('2_7', '2.7'),
    ('2_8', '2.8'),
    ('2_9', '2.9'),
    ('3_0', '3.0'),
    ('3_1', '3.1'),
    ('3_2', '3.2'),
    ('3_3', '3.3'),
    ('3_4', '3.4'),
    ('3_5', '3.5'),
    ('3_6', '3.6'),
    ('3_7', '3.7'),
    ('3_8', '3.8'),
    ('3_9', '3.9'),
    ('4_0', '4.0'),
)

TEXT_ATTENDANCE_CHOICES = (
    ('Never', 'Never'),
    ('1to5', 'Between 1 and 5 times'),
    ('5to10', 'Between 5 and 10 times'),
    ('morethan10', 'Greater than 10 times'),
)

TEXT_COLLEGE_CHOICES = (
    ('LSA', 'LSA'),
    ('Engineering', 'Engineering'),
    ('Kinesiology', 'Kinesiology'),
    ('Other', 'Other'),
)

INT_SEMESTERSCOMPLETED_CHOICES = (
    ('9', 'More than 8 semesters'),
)

TEXT_APBIO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

TEXT_ECOACH_COMPONENTS_CHOICES = (
    ('advice_students', 'Advice from students'),
    ('advice_professors', 'Advice from professors'),
    ('study_tips', 'General study tips'),
    ('problem_roulette', 'Problem Roulette'),
    ('video_content', 'Video content'),
    ('grade_prediction_tool', 'Grade prediction tool'),
    ('grade_calculator', 'Grade calculator tool'),
    ('class_calendar', 'Class calendar'),
)

CTEXT_COLLEGE_CHOICES = (
    ('LSA', 'LSA'),
    ('Engineering', 'Engineering'),
    ('Kinesiology', 'Kinesiology'),
    ('Other', 'Other'),
)

TEXT_INVOLVEDIN_CHOICES = (
    ('Greek', 'Greek Life (Sororities/Fraternities)'),
    ('Sports', 'Sports/Club Sports'),
    ('Religious', 'Religious Organizations'),
    ('Research', 'Research (Thesis, UROP, Lab work)'),
    ('Volunteering', 'Volunteering'),
    ('Music_Art', 'Music/Art'),
    ('Other', 'Other Student Clubs/Organzations'),
)

OPT_OUT_CHOICES = (
    ('0', 'Opt in'),
    ('1', 'Opt out'),
)

CTEXT_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

INT_GPASURVEY_CHOICES = (
    ('2_0', '2.0 or lower'),
    ('2_1', '2.1'),
    ('2_2', '2.2'),
    ('2_3', '2.3'),
    ('2_4', '2.4'),
    ('2_5', '2.5'),
    ('2_6', '2.6'),
    ('2_7', '2.7'),
    ('2_8', '2.8'),
    ('2_9', '2.9'),
    ('3_0', '3.0'),
    ('3_1', '3.1'),
    ('3_2', '3.2'),
    ('3_3', '3.3'),
    ('3_4', '3.4'),
    ('3_5', '3.5'),
    ('3_6', '3.6'),
    ('3_7', '3.7'),
    ('3_8', '3.8'),
    ('3_9', '3.9'),
    ('4_0', '4.0'),
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

TEXT_APCHEM_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

TEXT_POSTCOLLEGE_CHOICES = (
    ('Employment', 'Employment'),
    ('Med_School', 'Medical School or other Health-related Professional School'),
    ('Dent_School', 'Dental School'),
    ('Education', 'Education (teaching, policy, or a certification program)'),
    ('Grad_Life_Sci', 'Graduate School in a Life Science discipline'),
    ('Grad_Other', 'Graduate School in another discipline'),
    ('IDK', "Unsure/I don't know"),
    ('Other', 'Other'),
)

TEXT_EMPLOYMENT_CHOICES = (
    ('No_Job', 'I do not have a job'),
    ('Part_Time', 'I work a part-time job (20 hours or less a week)'),
    ('Full_Time', 'I work a full-time job (more than 20 hours a week)'),
)

TEXT_PRED_CHOICES = (
    ('8', 'A'),
    ('7', 'A-'),
    ('6', 'B+'),
    ('5', 'B'),
    ('4', 'B-'),
    ('3', 'C+'),
    ('2', 'C'),
    ('1', 'C-'),
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

INT_CONFIDENCE_CHOICES = (
    ('0', '0<br>Not confident at all'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10<br>Extremely confident'),
)

TEXT_REASON_CHOICES = (
    ('Possible_Concentrate_req', 'I am considering this subject as my concentration'),
    ('Concentration_req', 'This is a course required by my concentration'),
    ('Grad_req', 'I need this class to prepare for my graduate/professional program'),
    ('Credit', 'For a specific credit (NS, QR, etc.)'),
    ('Interest', "I'm taking this class because of my interest in the subject"),
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

INT_FSLEASTVALUABLE_CHOICES = (
    ('1', 'Advice From students'),
    ('2', 'Advice From professors'),
    ('3', 'General study tips'),
    ('4', 'Problem roulette'),
    ('5', 'Video content'),
    ('6', 'Grade prediction tool'),
    ('7', 'Grade calculator tool'),
    ('8', 'Class calendar'),
)

CTEXT_EMPLOYMENT_STATUS_CHOICES = (
    ('No_Job', 'I do not have a job'),
    ('Part_Time', 'I work a part-time job (20 hours or less a week)'),
    ('Full_Time', 'I work a full-time job (more than 20 hours a week)'),
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

CTEXT_YES_NO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

INT_USAGE_CHOICES = (
    ('5', 'Daily'),
    ('4', 'Every couple of days'),
    ('3', 'Once a week'),
    ('2', 'Once every few weeks'),
    ('1', 'Mostly after exams'),
)

INT_SUBJECTINTEREST_CHOICES = (
    ('0', '0<br>Not at all interested'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10<br>Extremely interested'),
)

TEXT_CONCENTRATE_CHOICES = (
    ('Engineering', 'Engineering'),
    ('Physics', 'Physics/Astrophysics'),
    ('Chemistry', 'Chemistry'),
    ('Biology', 'Biology'),
    ('Biology_MCDB', 'Biology MCDB'),
    ('Biology_EEB', 'Biology EEB'),
    ('Health', 'Health-related Field (Physical Therapy, Pharmacology, Nursing, etc.)'),
    ('Humanities', 'Humanities'),
    ('Math', 'Mathematics'),
    ('Neurosci', 'Neuroscience'),
    ('Social_Science_not_Psych', 'Social Science (excluding Psychology)'),
    ('Psych_BBCS', 'Psychology or BBCS'),
    ('Education', 'Education'),
    ('IDK', 'I do not know'),
    ('Other', 'Other'),
)

GRADE_DIST_CHOICES = (
    ('8', 'A'),
    ('7', 'A-'),
    ('6', 'B+'),
    ('5', 'B'),
    ('4', 'B-'),
    ('3', 'C+'),
    ('2', 'C'),
    ('1', 'C-'),
)

CTEXT_CLASS_STANDING_CHOICES = (
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
)

TEXT_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

INT_GOAL_CHOICES = (
    ('8', 'A'),
    ('7', 'A-'),
    ('6', 'B+'),
    ('5', 'B'),
    ('4', 'B-'),
    ('3', 'C+'),
    ('2', 'C'),
    ('1', 'C-'),
)

TEXT_SLCENROLLED_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

TEXT_DECLARED_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
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

INT_BIRTHMO_CHOICES = (
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

TEXT_CLASSSTANDING_CHOICES = (
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
)


class Source1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_source1'
    SLC_Enrolled = models.CharField(max_length=3, choices=TEXT_SLCENROLLED_CHOICES, null=True, blank=True)
    Reg_Enrolled = models.IntegerField(null=True, blank=True)
    Reg_GPA = models.FloatField(null=True, blank=True)
    Reg_Gender = models.CharField(max_length=5, null=True, blank=True)
    Reg_Acad_Level = models.CharField(max_length=20, null=True, blank=True)
    Signup_Opt_Out = models.IntegerField(null=True, blank=True)
    AP_Bio = models.CharField(max_length=3, choices=TEXT_APBIO_CHOICES, null=True, blank=True)
    AP_Chem = models.CharField(max_length=3, choices=TEXT_APCHEM_CHOICES, null=True, blank=True)
    Confidence = models.CharField(max_length=2, choices=INT_CONFIDENCE_CHOICES, null=True, blank=True)
    Goal_Grade = models.IntegerField(null=True, blank=True)
    Reason__Possible_Concentrate_req = models.NullBooleanField()
    Reason__Concentration_req = models.NullBooleanField()
    Reason__Grad_req = models.NullBooleanField()
    Reason__Credit = models.NullBooleanField()
    Reason__Interest = models.NullBooleanField()
    Subject_Interest = models.CharField(max_length=2, choices=INT_SUBJECTINTEREST_CHOICES, null=True, blank=True)
    Attendance_Anticipated = models.CharField(max_length=10, choices=TEXT_ATTENDANCE_CHOICES, null=True, blank=True)
    FS_MostValuable__advice_students = models.NullBooleanField()
    FS_MostValuable__advice_professors = models.NullBooleanField()
    FS_MostValuable__study_tips = models.NullBooleanField()
    FS_MostValuable__problem_roulette = models.NullBooleanField()
    FS_MostValuable__video_content = models.NullBooleanField()
    FS_MostValuable__grade_prediction_tool = models.NullBooleanField()
    FS_MostValuable__grade_calculator = models.NullBooleanField()
    FS_MostValuable__class_calendar = models.NullBooleanField()
    FS_LeastValuable__advice_students = models.NullBooleanField()
    FS_LeastValuable__advice_professors = models.NullBooleanField()
    FS_LeastValuable__study_tips = models.NullBooleanField()
    FS_LeastValuable__problem_roulette = models.NullBooleanField()
    FS_LeastValuable__video_content = models.NullBooleanField()
    FS_LeastValuable__grade_prediction_tool = models.NullBooleanField()
    FS_LeastValuable__grade_calculator = models.NullBooleanField()
    FS_LeastValuable__class_calendar = models.NullBooleanField()
    FS_Changes = models.TextField(null=True, blank=True)
    FS_Usage = models.CharField(max_length=1, choices=INT_USAGE_CHOICES, null=True, blank=True)
    FS_Challenges = models.TextField(null=True, blank=True)
    Exam1_FR = models.FloatField(null=True, blank=True)
    Exam1_MC = models.FloatField(null=True, blank=True)
    Exam1_Score = models.FloatField(null=True, blank=True)
    Exam1_ClassAvg = models.FloatField(null=True, blank=True)
    Exam2_FR = models.FloatField(null=True, blank=True)
    Exam2_MC = models.FloatField(null=True, blank=True)
    Exam2_Score = models.FloatField(null=True, blank=True)
    Exam2_ClassAvg = models.FloatField(null=True, blank=True)
    Exam3_FR = models.FloatField(null=True, blank=True)
    Exam3_MC = models.FloatField(null=True, blank=True)
    Exam3_Score = models.FloatField(null=True, blank=True)
    Exam3_ClassAvg = models.FloatField(null=True, blank=True)
    Exam4_FR = models.FloatField(null=True, blank=True)
    Exam4_MC = models.FloatField(null=True, blank=True)
    Exam4_Score = models.FloatField(null=True, blank=True)
    Exam4_ClassAvg = models.FloatField(null=True, blank=True)
    Project1_Grade = models.FloatField(null=True, blank=True)
    Project2_Grade = models.FloatField(null=True, blank=True)
    Project3_Grade = models.FloatField(null=True, blank=True)
    iClicker_Grade = models.FloatField(null=True, blank=True)
    CellMap_Grade = models.FloatField(null=True, blank=True)
    Num_PR_Questions = models.IntegerField(null=True, blank=True)
    Grade_PR_Questions = models.FloatField(null=True, blank=True)
    MCDB310FinalGradeLetter = models.FloatField(null=True, blank=True)
    MCDB310FinalGradeNumber = models.FloatField(null=True, blank=True)
    dist_id = models.CharField(max_length=50, null=True, blank=True)
    dist_id2 = models.CharField(max_length=50, null=True, blank=True)
    dist_id3 = models.CharField(max_length=50, null=True, blank=True)
    dist_id4 = models.CharField(max_length=50, null=True, blank=True)
    Exam1_Score_Percent = models.FloatField(null=True, blank=True)
    Exam2_Score_Percent = models.FloatField(null=True, blank=True)
    Exam3_Score_Percent = models.FloatField(null=True, blank=True)
    Exam4_Score_Percent = models.FloatField(null=True, blank=True)
    Pred_MostProb_Initial = models.IntegerField(null=True, blank=True)
    Pred_MostProb_PostExam1 = models.IntegerField(null=True, blank=True)
    Pred_MostProb_PostExam2 = models.IntegerField(null=True, blank=True)
    Pred_MostProb_PostExam3 = models.IntegerField(null=True, blank=True)

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


