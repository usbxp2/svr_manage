from django.forms import Form, ModelForm
from app import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customers
        exclude = ()
    #给form加点样式
    def __init__(self, *args, **kwargs):
        super(CustomerModelForm, self).__init__(*args, **kwargs)
        #sefl.base_fields是所有的fields集合，循环给每个field都加上样式
        #继承后重写field给它加点class样式
        for field_name in self.base_fields:
            field =self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class CloudModelForm(ModelForm):
    class Meta:
        model = models.Cloud
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(CloudModelForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class HostModelForm(ModelForm):
    class Meta:
        model = models.Hosts
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(HostModelForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})

class ProjectModelForm(ModelForm):
    class Meta:
        model = models.Projects
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(ProjectModelForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})
