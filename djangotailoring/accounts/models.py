import sys

from django.db import models, transaction

from djangotailoring.accounts.accesscodes import Code, BasicAccessCode

class GroupAccessCode(models.Model):
    groupcode = models.TextField(max_length=30)
    usage_limit = models.IntegerField(default=-1)
    
    code_class = Code
    
    @transaction.commit_on_success
    def generate_new_subcode(self):
        usage_limit = self.usage_limit
        if self.usage_limit < 0:
            usage_limit = sys.maxint
        if self.generatedaccesscode_set.count() >= usage_limit:
            return None
        new_code = self.code_class.new_code()
        self.generatedaccesscode_set.create(accesscode=new_code.accesscode)
        return new_code
    

class GeneratedAccessCode(models.Model):
    accesscode = models.TextField(max_length=30)
    groupcode = models.ForeignKey(GroupAccessCode)


class BasicGroupAccessCode(GroupAccessCode):
    code_class = BasicAccessCode
    
    class Meta:
        proxy = True
    
