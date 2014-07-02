from django.db import models
from django.contrib.auth.models import User

# table format source data
from djangotailoring.models import SubjectData

# Create your models here.

# python ../manage.py makemtsmodel > MODEL.OUT (results go below here)

_ACT_REF_01_CHOICES = (
    ('-1', 'try it out.'),
    ('1', 'think it through.'),
)

INT_SNS_INT_08_CHOICES = (
    ('-1', 'master one way of doing it.'),
    ('1', 'come up with new ways of doing it.'),
)

INT_SNS_INT_09_CHOICES = (
    ('-1', 'sensible.'),
    ('1', 'imaginative.'),
)

INT_SNS_INT_02_CHOICES = (
    ('-1', 'that deals with facts and real life situations.'),
    ('1', 'that deals with ideas and theories.'),
)

INT_SEQ_GLO_03_CHOICES = (
    ('-1', 'I usually work my way to the solutions one step at a time.'),
    ('1', 'I often just see the solutions but then have to struggle to figure out the steps to get to \r\nthem.'),
)

INT_ACT_REF_10_CHOICES = (
    ('-1', 'try it out.'),
    ('1', 'think it through.'),
)

INT_ACT_REF_08_CHOICES = (
    ('-1', 'something I have done.'),
    ('1', 'something I have thought a lot about.'),
)

INT_VIS_VRB_10_CHOICES = (
    ('-1', 'watch television.'),
    ('1', 'read a book.'),
)

INT_VIS_VRB_11_CHOICES = (
    ('-1', 'easily and fairly accurately.'),
    ('1', 'with difficulty and without much detail.'),
)

INT_SNS_INT_03_CHOICES = (
    ('-1', 'to learn facts.'),
    ('1', 'to learn concepts.'),
)

INT_VIS_VRB_01_CHOICES = (
    ('-1', 'a picture.'),
    ('1', 'words.'),
)

INT_VIS_VRB_08_CHOICES = (
    ('-1', 'charts or graphs.'),
    ('1', 'text summarizing the results.'),
)

_ACT_REF_10_CHOICES = (
    ('-1', 'outgoing.'),
    ('1', 'reserved.'),
)

INT_ACT_REF_01_CHOICES = (
    ('-1', '-1'),
    ('1', '1'),
)

INT_SEQ_GLO_11_CHOICES = (
    ('-1', 'think of the steps in the solution process.'),
    ('1', 'think of possible consequences or applications of the solution in a wide range of areas.'),
)

INT_SNS_INT_10_CHOICES = (
    ('-1', 'concrete material (facts, data).'),
    ('1', 'abstract material (concepts, theories).'),
)

INT_ACT_REF_06_CHOICES = (
    ('-1', 'in a study group.'),
    ('1', 'alone.'),
)

INT_ACT_REF_07_CHOICES = (
    ('-1', 'try things out.'),
    ('1', u'think about how I\u2019m going to do it.'),
)

INT_TO_LETTER_EXPECTED_GRADE_CHOICES = (
    ('5', 'C- or lower'),
    ('6', 'C'),
    ('7', 'C+'),
    ('8', 'B-'),
    ('9', 'B'),
    ('10', 'B+'),
    ('11', 'A-'),
    ('12', 'A'),
    ('13', 'A+'),
)

INT_SNS_INT_06_CHOICES = (
    ('-1', 'careful about the details of my work.'),
    ('1', 'creative about how to do my work.'),
)

INT_ACT_REF_09_CHOICES = (
    ('-1', u'have \u201cgroup brainstorming\u201d where everyone contributes ideas.'),
    ('1', 'brainstorm individually and then come together as a group to compare ideas.'),
)

INT_EXAM_2_PREP_RESOURCES_CHOICES = (
    ('0', 'reviewed the <b>lecture notes</b>'),
    ('1', 'watched some <b>Blue Review</b> captured lectures'),
    ('2', 'o reviewed past <b>required HW</b> problems'),
    ('3', 'reviewed past <b>recommended HW</b> problems'),
    ('4', 'tried some past exam questions on ,b>Problem Roulette</b>'),
    ('5', 'o practiced identifying which statistical procedure would be appropriate with <b>Name That Scenario</b>'),
    ('6', 'attended <b>office hours</b> during exam week'),
    ('7', 'reviewed some <b>lab materials</b> (ILPs)'),
    ('8', 'read some parts of the <b>textbook</b>'),
    ('9', 'discussed material with other students in the class (like <b>study group</b>)'),
    ('10', 'worked questions from the <b>practice exams</b> (from the lab workbook)'),
)

INT_ACT_REF_02_CHOICES = (
    ('-1', 'talk about it.'),
    ('1', 'think about it.'),
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

CTEXT_COLLEGE_CHOICES = (
    ('LSA', 'LSA'),
    ('Engineering', 'Engineering'),
    ('Kinesiology', 'Kinesiology'),
    ('Other', 'Other'),
)

CTEXT_YES_NO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

_SEQ_GLO_10_CHOICES = (
    ('-1', 'somewhat helpful to me.'),
    ('1', 'very helpful to me.'),
)

INT_TO_LETTER_GOAL_GRADE_CHOICES = (
    ('1', 'C- or lower'),
    ('2', 'C'),
    ('3', 'C+'),
    ('4', 'B-'),
    ('5', 'B'),
    ('6', 'B+'),
    ('7', 'A-'),
    ('8', 'A or A+'),
)

INT_SUBJECT_INTEREST_CHOICES = (
    ('0', '0-Not at all interested'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10-Extremely interested'),
)

INT_SEQ_GLO_07_CHOICES = (
    ('-1', 'focus on details and miss the big picture.'),
    ('1', 'try to understand the big picture before getting into the details.'),
)

CTEXT_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

INT_VIS_VRB_05_CHOICES = (
    ('-1', 'what I see.'),
    ('1', 'what I hear.'),
)

OPT_OUT_CHOICES = (
    ('0', 'Opt in'),
    ('1', 'Opt out'),
)

CINT_SEMSESTERS_COMPLETED_CHOICES = (
    ('9', 'More than 8 semesters'),
)

INT_VIS_VRB_09_CHOICES = (
    ('-1', 'what they looked like.'),
    ('1', 'what they said about themselves.'),
)

INT_SEMESTER_FREQ_CHOICES = (
    ('0', 'never'),
    ('1', 'once or twice during the semester'),
    ('2', 'monthly'),
    ('3', 'weekly'),
    ('4', 'multiple times per week'),
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

INT_SEQ_GLO_02_CHOICES = (
    ('-1', 'all the parts, I understand the whole thing.'),
    ('1', 'the whole thing, I see how the parts fit.'),
)

INT_VIS_VRB_04_CHOICES = (
    ('-1', 'who put a lot of diagrams on the board.'),
    ('1', 'who spend a lot of time explaining.'),
)

INT_SNS_INT_05_CHOICES = (
    ('-1', 'certainty.'),
    ('1', 'theory.'),
)

INT_YES_NO_CHOICES = (
    ('0', 'no'),
    ('1', 'yes'),
)

INT_CONFIDENCE_CHOICES = (
    ('1', 'very doubtful'),
    ('2', 'somewhat doubtful'),
    ('3', 'somewhat confident'),
    ('4', 'confident'),
    ('5', 'very confident'),
)

TEXT_OPT_OUT_CHOICES = (
    ('In', 'Yes, take me to the survey now!'),
    ('Out', "No thanks, I'll opt out and understand that if I use ecaoch it will only offer generic advice."),
)

INT_ACT_REF_04_CHOICES = (
    ('-1', 'I have usually gotten to know many of the students.'),
    ('1', 'I have rarely gotten to know many of the students.'),
)

INT_TRUE_FALSE_CHOICES = (
    ('1', 'True'),
    ('0', 'False'),
)

INT_ACT_REF_03_CHOICES = (
    ('-1', 'jump in and contribute ideas.'),
    ('1', 'sit back and listen.'),
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

INT_VIS_VRB_07_CHOICES = (
    ('-1', 'the picture.'),
    ('1', 'what the instructor said about it.'),
)

INT_VIS_VRB_06_CHOICES = (
    ('-1', 'a map.'),
    ('1', 'written instructions.'),
)

INT_ACT_REF_05_CHOICES = (
    ('-1', 'start working on the solution immediately.'),
    ('1', 'try to fully understand the problem first.'),
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

INT_MLECTUREBOOK_CHOICES = (
    ('0', 'none'),
    ('1', 'hw'),
    ('2', 'both'),
)

INT_MTEXTBOOK_CHOICES = (
    ('0', 'none'),
    ('1', 'book'),
    ('2', 'pack'),
)

INT_VIS_VRB_03_CHOICES = (
    ('-1', 'look over the pictures and charts carefully.'),
    ('1', 'focus on the written text.'),
)

INT_SEQ_GLO_06_CHOICES = (
    ('-1', u'at a fairly regular pace. If I study hard, I\u2019ll \u201cget it.\u201d'),
    ('1', u'in fits and starts. I\u2019ll be totally confused and then suddenly it all \u201cclicks.\u201d'),
)

INT_SNS_INT_07_CHOICES = (
    ('-1', 'clearly say what they mean.'),
    ('1', 'say things in creative, interesting ways.'),
)

CTEXT_EMPLOYMENT_STATUS_CHOICES = (
    ('No_Job', 'I do not have a job'),
    ('Part_Time', 'I work a part-time job (20 hours or less a week)'),
    ('Full_Time', 'I work a full-time job (more than 20 hours a week)'),
)

INT_SNS_INT_01_CHOICES = (
    ('-1', 'realistic.'),
    ('1', 'innovative.'),
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

INT_SEQ_GLO_04_CHOICES = (
    ('-1', 'I think of the incidents and try to put them together to figure out the themes.'),
    ('1', 'I just know what the themes are when I finish reading and then I have to go back and find \r\nthe incidents that demonstrate them.'),
)

INT_SEQ_GLO_05_CHOICES = (
    ('-1', 'lay out the material in clear sequential steps.'),
    ('1', 'give me an overall picture and relate the material to other subjects.'),
)

INT_SNS_INT_11_CHOICES = (
    ('-1', 'I tend to repeat all my steps and check my work carefully.'),
    ('1', 'I find checking my work tiresome and have to force myself to do it'),
)

TEXT_GTD_CHOICES = (
    ('done', '-'),
)

INT_EXAM_2_PREP_SIMULATION_CHOICES = (
    ('0', 'None'),
    ('1', 'One'),
    ('2', 'Two'),
    ('3', 'Three'),
    ('4', 'Four'),
)

INT_ACT_REF_11_CHOICES = (
    ('-1', 'appeals to me.'),
    ('1', 'does not appeal to me.'),
)

CTEXT_CLASS_STANDING_CHOICES = (
    ('Freshman', 'Freshman'),
    ('Sophomore', 'Sophomore'),
    ('Junior', 'Junior'),
    ('Senior', 'Senior'),
)

INT_CONFIDENCE_IN_ABLILITY_CHOICES = (
    ('0', '0-Not at all confident'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10-Extremely confident'),
)

TEXT_GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

INT_SEQ_GLO_08_CHOICES = (
    ('-1', 'work on (think about or write) the beginning of the paper and progress forward.'),
    ('1', 'work on (think about or write) different parts of the paper and then order them.'),
)

INT_SEQ_GLO_09_CHOICES = (
    ('-1', 'stay focused on that subject, learning as much about it as I can.'),
    ('1', 'try to make connections between that subject and related subjects.'),
)

INT_INTEREST_AFTER_STATS250_CHOICES = (
    ('0', 'taking another statistics course'),
    ('1', 'learning more about majoring or minoring is statistics.'),
    ('2', 'neither (but glad to have finished this statistics course using ECoach).'),
)

INT_PERMISSION_TO_USE_EXAM_2_SELF_ADVICE_CHOICES = (
    ('2', 'Yes, you may use my name and picture.'),
    ('1', 'Yes, you may use my name.'),
    ('0', 'No, please do not use my name or picture.'),
)

INT_SEQ_GLO_10_CHOICES = (
    ('-1', 'somewhat helpful to me.'),
    ('1', 'appeals to me.'),
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

INT_VIS_VRB_02_CHOICES = (
    ('-1', 'pictures, diagrams, graphs, or maps.'),
    ('1', 'written directions or verbal information.'),
)

INT_SEQ_GLO_01_CHOICES = (
    ('-1', 'understand details of a subject but may be fuzzy about its overall structure.'),
    ('1', 'understand the overall structure but may be fuzzy about details.'),
)

INT_SNS_INT_04_CHOICES = (
    ('-1', 'something that teaches me new facts or tells me how to do something.'),
    ('1', 'something that gives me new ideas to think about.'),
)

INT_MYELLOW_CHOICES = (
    ('0', 'none'),
    ('1', 'printed'),
    ('2', 'card'),
)


class Source1(SubjectData):
    # add meta property
    class Meta: 
        db_table = 'mydata_source1'
    ECoach_helpful_study = models.IntegerField(null=True, blank=True)
    ECoach_helpful_exam = models.IntegerField(null=True, blank=True)
    ECoach_helpful_most = models.TextField(null=True, blank=True)
    ECoach_would_change = models.TextField(null=True, blank=True)
    ECoach_favorite_message = models.TextField(null=True, blank=True)
    interest_after_STATS250 = models.IntegerField(null=True, blank=True)
    Final_Course_Letter_Grade = models.CharField(max_length=20, null=True, blank=True)
    Method_1_Grade = models.FloatField(null=True, blank=True)
    Method_2_Grade = models.FloatField(null=True, blank=True)
    Reg_Enrolled = models.IntegerField(null=True, blank=True)
    Reg_GPA = models.FloatField(null=True, blank=True)
    Reg_Gender = models.CharField(max_length=5, null=True, blank=True)
    Reg_Acad_Level = models.CharField(max_length=20, null=True, blank=True)
    email_request_1 = models.IntegerField(null=True, blank=True)
    email_request_2 = models.IntegerField(null=True, blank=True)
    email_request_3 = models.IntegerField(null=True, blank=True)
    email_request_4 = models.IntegerField(null=True, blank=True)
    like_about_ecoach = models.TextField(null=True, blank=True)
    make_ecoach_better = models.TextField(null=True, blank=True)
    Signup_Opt_Out = models.IntegerField(null=True, blank=True)
    hw_hours = models.FloatField(null=True, blank=True)
    oh_expected = models.IntegerField(null=True, blank=True)
    study_partner = models.IntegerField(null=True, blank=True)
    Subject_Interest = models.IntegerField(null=True, blank=True)
    time_expectation = models.IntegerField(null=True, blank=True)
    Confidence = models.IntegerField(null=True, blank=True)
    confidence_grade = models.IntegerField(null=True, blank=True)
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
    gb_hw_practice = models.FloatField(null=True, blank=True)
    gb_hw01 = models.FloatField(null=True, blank=True)
    gb_hw02 = models.FloatField(null=True, blank=True)
    gb_hw03 = models.FloatField(null=True, blank=True)
    gb_hw04 = models.FloatField(null=True, blank=True)
    gb_hw05 = models.FloatField(null=True, blank=True)
    gb_hw06 = models.FloatField(null=True, blank=True)
    gb_hw07 = models.FloatField(null=True, blank=True)
    gb_hw08 = models.FloatField(null=True, blank=True)
    gb_hw09 = models.FloatField(null=True, blank=True)
    gb_hw10 = models.FloatField(null=True, blank=True)
    gb_hw11 = models.FloatField(null=True, blank=True)
    gb_hw_extra = models.FloatField(null=True, blank=True)
    gb_exam1 = models.FloatField(null=True, blank=True)
    gb_exam2 = models.FloatField(null=True, blank=True)
    gb_final = models.FloatField(null=True, blank=True)
    gb_lab00_attend = models.IntegerField(null=True, blank=True)
    gb_lab01_attend = models.IntegerField(null=True, blank=True)
    gb_lab02_attend = models.IntegerField(null=True, blank=True)
    gb_lab03_attend = models.IntegerField(null=True, blank=True)
    gb_lab04_attend = models.IntegerField(null=True, blank=True)
    gb_lab05_attend = models.IntegerField(null=True, blank=True)
    gb_lab06_attend = models.IntegerField(null=True, blank=True)
    gb_lab07_attend = models.IntegerField(null=True, blank=True)
    gb_lab08_attend = models.IntegerField(null=True, blank=True)
    gb_lab09_attend = models.IntegerField(null=True, blank=True)
    gb_lab10_attend = models.IntegerField(null=True, blank=True)
    gb_lab11_attend = models.IntegerField(null=True, blank=True)
    gb_lab12_attend = models.IntegerField(null=True, blank=True)
    gb_lab13_attend = models.IntegerField(null=True, blank=True)
    gb_prelab01 = models.IntegerField(null=True, blank=True)
    gb_prelab02 = models.IntegerField(null=True, blank=True)
    gb_prelab03 = models.IntegerField(null=True, blank=True)
    gb_prelab04 = models.IntegerField(null=True, blank=True)
    gb_prelab05 = models.IntegerField(null=True, blank=True)
    gb_prelab06 = models.IntegerField(null=True, blank=True)
    gb_prelab07 = models.IntegerField(null=True, blank=True)
    gb_prelab08 = models.IntegerField(null=True, blank=True)
    gb_prelab09 = models.IntegerField(null=True, blank=True)
    gb_prelab10 = models.IntegerField(null=True, blank=True)
    gb_prelab11 = models.IntegerField(null=True, blank=True)
    gb_prelab12 = models.IntegerField(null=True, blank=True)
    Exam1_Self_Advice = models.TextField(null=True, blank=True)
    Exam2_Self_Advice = models.TextField(null=True, blank=True)
    Permission_To_Use_Exam1_Self_Advice = models.IntegerField(null=True, blank=True)
    Permission_To_Use_Exam_2_Self_Advice = models.IntegerField(null=True, blank=True)
    Exam_2_Prep_Resources__0 = models.NullBooleanField()
    Exam_2_Prep_Resources__1 = models.NullBooleanField()
    Exam_2_Prep_Resources__2 = models.NullBooleanField()
    Exam_2_Prep_Resources__3 = models.NullBooleanField()
    Exam_2_Prep_Resources__4 = models.NullBooleanField()
    Exam_2_Prep_Resources__5 = models.NullBooleanField()
    Exam_2_Prep_Resources__6 = models.NullBooleanField()
    Exam_2_Prep_Resources__7 = models.NullBooleanField()
    Exam_2_Prep_Resources__8 = models.NullBooleanField()
    Exam_2_Prep_Resources__9 = models.NullBooleanField()
    Exam_2_Prep_Resources__10 = models.NullBooleanField()
    Exam_2_Prep_Simulation = models.IntegerField(null=True, blank=True)
    GSI_Name = models.CharField(max_length=20, null=True, blank=True)
    dist_values = models.TextField(null=True, blank=True)
    dist_values_after_Exam_2 = models.TextField(null=True, blank=True)
    Goal_Grade = models.IntegerField(null=True, blank=True)
    Expected_Grade = models.IntegerField(null=True, blank=True)
    mcalculator = models.IntegerField(null=True, blank=True)
    mamazonlecture = models.IntegerField(null=True, blank=True)
    mlecturebook = models.IntegerField(null=True, blank=True)
    mamazonlab = models.IntegerField(null=True, blank=True)
    mopenmi = models.IntegerField(null=True, blank=True)
    mopenmilab = models.IntegerField(null=True, blank=True)
    mtextbook = models.IntegerField(null=True, blank=True)
    myellow = models.IntegerField(null=True, blank=True)
    Lecture_Section = models.IntegerField(null=True, blank=True)
    sleep_01 = models.IntegerField(null=True, blank=True)
    sleep_02 = models.IntegerField(null=True, blank=True)
    sleep_03 = models.IntegerField(null=True, blank=True)
    sleep_04 = models.IntegerField(null=True, blank=True)
    sleep_05 = models.IntegerField(null=True, blank=True)
    sleep_06 = models.IntegerField(null=True, blank=True)
    sleep_07 = models.IntegerField(null=True, blank=True)
    sleep_08 = models.IntegerField(null=True, blank=True)
    sleep_09 = models.IntegerField(null=True, blank=True)
    sleep_10 = models.IntegerField(null=True, blank=True)
    sleep_11 = models.IntegerField(null=True, blank=True)
    sleep_12 = models.IntegerField(null=True, blank=True)
    rested_01 = models.IntegerField(null=True, blank=True)
    rested_02 = models.IntegerField(null=True, blank=True)
    rested_03 = models.IntegerField(null=True, blank=True)
    rested_04 = models.IntegerField(null=True, blank=True)
    rested_05 = models.IntegerField(null=True, blank=True)
    rested_06 = models.IntegerField(null=True, blank=True)
    rested_07 = models.IntegerField(null=True, blank=True)
    rested_08 = models.IntegerField(null=True, blank=True)
    rested_09 = models.IntegerField(null=True, blank=True)
    rested_10 = models.IntegerField(null=True, blank=True)
    rested_11 = models.IntegerField(null=True, blank=True)
    rested_12 = models.IntegerField(null=True, blank=True)
    ACT_REF_01 = models.IntegerField(null=True, blank=True)
    SNS_INT_01 = models.IntegerField(null=True, blank=True)
    VIS_VRB_01 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_01 = models.IntegerField(null=True, blank=True)
    ACT_REF_02 = models.IntegerField(null=True, blank=True)
    SNS_INT_02 = models.IntegerField(null=True, blank=True)
    VIS_VRB_02 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_02 = models.IntegerField(null=True, blank=True)
    ACT_REF_03 = models.IntegerField(null=True, blank=True)
    SNS_INT_03 = models.IntegerField(null=True, blank=True)
    VIS_VRB_03 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_03 = models.IntegerField(null=True, blank=True)
    ACT_REF_04 = models.IntegerField(null=True, blank=True)
    SNS_INT_04 = models.IntegerField(null=True, blank=True)
    VIS_VRB_04 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_04 = models.IntegerField(null=True, blank=True)
    ACT_REF_05 = models.IntegerField(null=True, blank=True)
    SNS_INT_05 = models.IntegerField(null=True, blank=True)
    VIS_VRB_05 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_05 = models.IntegerField(null=True, blank=True)
    ACT_REF_06 = models.IntegerField(null=True, blank=True)
    SNS_INT_06 = models.IntegerField(null=True, blank=True)
    VIS_VRB_06 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_06 = models.IntegerField(null=True, blank=True)
    ACT_REF_07 = models.IntegerField(null=True, blank=True)
    SNS_INT_07 = models.IntegerField(null=True, blank=True)
    VIS_VRB_07 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_07 = models.IntegerField(null=True, blank=True)
    ACT_REF_08 = models.IntegerField(null=True, blank=True)
    SNS_INT_08 = models.IntegerField(null=True, blank=True)
    VIS_VRB_08 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_08 = models.IntegerField(null=True, blank=True)
    ACT_REF_09 = models.IntegerField(null=True, blank=True)
    SNS_INT_09 = models.IntegerField(null=True, blank=True)
    VIS_VRB_09 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_09 = models.IntegerField(null=True, blank=True)
    ACT_REF_10 = models.IntegerField(null=True, blank=True)
    SNS_INT_10 = models.IntegerField(null=True, blank=True)
    VIS_VRB_10 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_10 = models.IntegerField(null=True, blank=True)
    ACT_REF_11 = models.IntegerField(null=True, blank=True)
    SNS_INT_11 = models.IntegerField(null=True, blank=True)
    VIS_VRB_11 = models.IntegerField(null=True, blank=True)
    SEQ_GLO_11 = models.IntegerField(null=True, blank=True)

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


