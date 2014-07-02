# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Source1.dist_id2'
        db.add_column('mydata_source1', 'dist_id2',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.dist_id3'
        db.add_column('mydata_source1', 'dist_id3',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.dist_id4'
        db.add_column('mydata_source1', 'dist_id4',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.Exam1_Score_Percent'
        db.add_column('mydata_source1', 'Exam1_Score_Percent',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.Exam2_Score_Percent'
        db.add_column('mydata_source1', 'Exam2_Score_Percent',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.Exam3_Score_Percent'
        db.add_column('mydata_source1', 'Exam3_Score_Percent',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Source1.Exam4_Score_Percent'
        db.add_column('mydata_source1', 'Exam4_Score_Percent',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Source1.dist_id2'
        db.delete_column('mydata_source1', 'dist_id2')

        # Deleting field 'Source1.dist_id3'
        db.delete_column('mydata_source1', 'dist_id3')

        # Deleting field 'Source1.dist_id4'
        db.delete_column('mydata_source1', 'dist_id4')

        # Deleting field 'Source1.Exam1_Score_Percent'
        db.delete_column('mydata_source1', 'Exam1_Score_Percent')

        # Deleting field 'Source1.Exam2_Score_Percent'
        db.delete_column('mydata_source1', 'Exam2_Score_Percent')

        # Deleting field 'Source1.Exam3_Score_Percent'
        db.delete_column('mydata_source1', 'Exam3_Score_Percent')

        # Deleting field 'Source1.Exam4_Score_Percent'
        db.delete_column('mydata_source1', 'Exam4_Score_Percent')


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
        'mydata6.common1': {
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
        'mydata6.emptysource': {
            'Meta': {'object_name': 'EmptySource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'db_column': "'user_id'", 'on_delete': 'models.SET_NULL', 'to_field': "'username'", 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'})
        },
        'mydata6.source1': {
            'AP_Bio': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'AP_Chem': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'Attendance_Anticipated': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'CellMap_Grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Confidence': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'Exam1_ClassAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam1_FR': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam1_MC': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam1_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam1_Score_Percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam2_ClassAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam2_FR': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam2_MC': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam2_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam2_Score_Percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam3_ClassAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam3_FR': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam3_MC': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam3_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam3_Score_Percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam4_ClassAvg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam4_FR': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam4_MC': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam4_Score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Exam4_Score_Percent': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'FS_Challenges': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FS_Changes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__advice_professors': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__advice_students': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__class_calendar': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__grade_calculator': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__grade_prediction_tool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__problem_roulette': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__study_tips': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_LeastValuable__video_content': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__advice_professors': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__advice_students': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__class_calendar': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__grade_calculator': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__grade_prediction_tool': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__problem_roulette': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__study_tips': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_MostValuable__video_content': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'FS_Usage': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'Goal_Grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Grade_PR_Questions': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MCDB310FinalGradeLetter': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'MCDB310FinalGradeNumber': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Source1', 'db_table': "'mydata_source1'"},
            'Num_PR_Questions': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_MostProb_Initial': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_MostProb_PostExam1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_MostProb_PostExam2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Pred_MostProb_PostExam3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Project1_Grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Project2_Grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Project3_Grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Reason__Concentration_req': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reason__Credit': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reason__Grad_req': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reason__Interest': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reason__Possible_Concentrate_req': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_Acad_Level': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'Reg_Enrolled': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_GPA': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'Reg_Gender': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'SLC_Enrolled': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'Signup_Opt_Out': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'Subject_Interest': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'dist_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dist_id2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dist_id3': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dist_id4': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'iClicker_Grade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'db_column': "'user_id'", 'on_delete': 'models.SET_NULL', 'to_field': "'username'", 'to': "orm['auth.User']", 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['mydata6']