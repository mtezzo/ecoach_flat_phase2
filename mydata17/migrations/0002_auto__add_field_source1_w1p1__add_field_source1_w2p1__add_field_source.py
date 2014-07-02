# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source1.w1p1'
        db.add_column('mydata_source1', 'w1p1',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w2p1'
        db.add_column('mydata_source1', 'w2p1',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w2p2'
        db.add_column('mydata_source1', 'w2p2',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w3p1'
        db.add_column('mydata_source1', 'w3p1',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w3p2'
        db.add_column('mydata_source1', 'w3p2',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w4p1'
        db.add_column('mydata_source1', 'w4p1',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.w4p2'
        db.add_column('mydata_source1', 'w4p2',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source1.w1p1'
        db.delete_column('mydata_source1', 'w1p1')

        # Deleting field 'Source1.w2p1'
        db.delete_column('mydata_source1', 'w2p1')

        # Deleting field 'Source1.w2p2'
        db.delete_column('mydata_source1', 'w2p2')

        # Deleting field 'Source1.w3p1'
        db.delete_column('mydata_source1', 'w3p1')

        # Deleting field 'Source1.w3p2'
        db.delete_column('mydata_source1', 'w3p2')

        # Deleting field 'Source1.w4p1'
        db.delete_column('mydata_source1', 'w4p1')

        # Deleting field 'Source1.w4p2'
        db.delete_column('mydata_source1', 'w4p2')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mydata17.common1': {
            'BirthDay': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'BirthMo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'BirthYr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Class_Standing': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'College': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'College_Other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Concentrate_Other': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Concentrate__Biology': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Biology_EEB': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Biology_MCDB': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Chemistry': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Education': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Engineering': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Health': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Humanities': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__IDK': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Math': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Neurosci': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Other': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Physics': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Psych_BBCS': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Social_Science_not_Psych': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Concentrate__Stats': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Cum_GPA_Survey': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Declared': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'Employment': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'First_Name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'High_School_CumGPA': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Greek': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Music_Art': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Other': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Religious': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Research': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Sports': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Involved_In__Volunteering': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Last_Name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Common1', 'db_table': "'mydata_common1'"},
            'Other_Commitment': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'Parent_Ed': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'Post_College': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'Semesters_Completed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uniqname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'db_column': "'user_id'", 'on_delete': 'models.SET_NULL', 'to_field': "'username'", 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'})
        },
        'mydata17.emptysource': {
            'Meta': {'object_name': 'EmptySource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'db_column': "'user_id'", 'on_delete': 'models.SET_NULL', 'to_field': "'username'", 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'})
        },
        'mydata17.source1': {
            'ACT_Math': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Another_Hard_Class': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'Attitude_Anxiety': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Attitude_Exams': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Attitude_Math': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Attitude_Physics_Exp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Attitude_Physics_Noexp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Confidence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Confidence_PreExam1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Confidence_PreExam2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Confidence_PreExam3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Confidence_PreFinal': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Course': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Distribution_ID_135': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Distribution_ID_140': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Distribution_ID_235': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Distribution_ID_240': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Exam_1_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam_2_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam_3_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam_Final_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FCI_PostTest': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FCI_PreTest': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_ECoach_Change': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_ECoach_ExamPrep': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_ECoach_Helpful': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_ECoach_StudyHabits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PeerAdvice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PhysicsHelpRoom_Attend': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PhysicsHelpRoom_Change': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PhysicsHelpRoom_Helpful': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PhysicsHelpRoom_Reason': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_PhysicsHelpRoom_Reason_Other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_StudyGroup_Attend': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_StudyGroup_Change': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_StudyGroup_Helpful': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam1_StudyGroup_New': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam2_PeerAdvice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackExam3_PeerAdvice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_Change': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_Confidence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_ExamPrep': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_Helpful': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_Major': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_OtherCourses_Text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_OtherCourses_YesNo': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_PeerAdvice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FeedbackFinal_StudyHabits': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Final_Course_Grade_Letter': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Final_Course_Grade_Perc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_Grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_Grade_Reset_initial': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_Grade_Reset_postexam1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_Grade_Reset_postexam2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_Grade_Reset_postexam3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam1_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam1_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam1_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam2_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam2_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam2_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam3_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam3_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreExam3_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreFinal_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreFinal_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Goal_PreFinal_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'GradeDistribution': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'GradeDistribution_LeftShade': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'GradeDistribution_Peak': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'GradeDistribution_RightShade': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'HS_Activity': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'HS_Activity_Other': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'HS_Math': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'HS_Math_Other': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Learner': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'MP_Name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'MP_PreExam_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MP_PreExam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MP_PreExam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MP_Time_PreExam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MP_Time_PreExam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Source1', 'db_table': "'mydata_source1'"},
            'Movie': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'Movie_Other': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'PT1_ApplyingMath': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_ConceptualProbs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_Notecard': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__bookprobs': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__lecturenotes': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__lecturevideos': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__masteringphysics': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__none': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__officehours': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__outsideresource': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__physicshelproom': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__practiceexam': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__problemroulette': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__readbook': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_PreviousStudy__studygroup': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_ProbConfident_135': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbConfident_140': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbConfident_235': ('django.db.models.fields.CharField', [], {'max_length': '23', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbConfident_240': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbSolvingStep': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle2_135': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle2_140': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle2_235': ('django.db.models.fields.CharField', [], {'max_length': '23', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle2_240': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggleImprovedConf': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle_135': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle_140': ('django.db.models.fields.CharField', [], {'max_length': '14', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle_235': ('django.db.models.fields.CharField', [], {'max_length': '23', 'null': 'True', 'blank': 'True'}),
            'PT1_ProbStruggle_240': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'PT1_Timelimit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Participation_PreExam_1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Participation_PreExam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Participation_PreExam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Partner': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'Past_Physics': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Past_Physics_Experience': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Past_Physics_When': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'PreMathTest': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Exam1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Exam2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Exam3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Final': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Initial_135': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Initial_140': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Initial_235': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_Grade_Initial_240': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ProblemRoulette_PreExam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ProblemRoulette_PreExam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ProblemRoulette_Time_PreExam_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ProblemRoulette_Time_PreExam_3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Reason': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'Reflection_PreExam2_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reflection_PreExam2_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reflection_PreExam3_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reflection_PreExam3_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reflection_PreFinal_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reflection_PreFinal_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_Acad_Level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Reg_Course': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_Enrolled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_GPA': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_Gender': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'SAT_Math': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'SLC_Interest': ('django.db.models.fields.CharField', [], {'max_length': '17', 'null': 'True', 'blank': 'True'}),
            'Signup_Opt_Out': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_1': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_10': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_11': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_12': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_13': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_14': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_2': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_3': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_4': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_5': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_6': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_7': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_8': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'Writing_Prompt_9': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redo_exam1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'redo_exam2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'redo_exam3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ssg_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'db_column': "'user_id'", 'on_delete': 'models.SET_NULL', 'to_field': "'username'", 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'}),
            'vote_exam1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vote_exam2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vote_exam3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w1p1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w2p1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w2p2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w3p1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w3p2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w4p1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'w4p2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mydata17']