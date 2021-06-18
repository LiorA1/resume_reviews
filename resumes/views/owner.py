from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """


# template names in:
# https://docs.djangoproject.com/en/3.1/topics/auth/default/#module-django.contrib.auth.views


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # https://stackoverflow.com/questions/21652073/django-how-to-set-a-hidden-field-on-a-generic-create-view
    # https://stackoverflow.com/questions/19051830/a-better-way-of-setting-values-in-createview
    def form_valid(self, form):
        print('OwnerCreateView:form_valid called')
        
        form.instance.author = self.request.user
        
        return super(OwnerCreateView, self).form_valid(form)


class ParentOwnerCreateView(OwnerCreateView):
    """
    Sub-class of the OwnerCreateView, that redirect to its own detailview(?)
    """


class ChildOwnerCreateView(OwnerCreateView):
    """
    Sub-class of OwnerCreateView, that abstract the logic of creating an object 
    from the parent page/view.
    """

    #find what type is the parent
    parent_model = None
    parent_reverse_prefix = None
    parent_pk = None

    #override the form_valid method
    def form_valid(self, form):
        try:
            self.parent_pk = self.kwargs.get('pk', None)
            currentParent = get_object_or_404(self.parent_model, id=self.parent_pk)
            
            # find the field from the type of the parent and popluate it
            setattr(form.instance, self.parent_model.__name__.lower(), currentParent)
        except Exception as e:
            print("==============")
            print(e, type(e))
            print("==============")

        return super(ChildOwnerCreateView, self).form_valid(form)
    

    def get_success_url(self):
        try:
            url = reverse(self.parent_reverse_prefix, args=[self.parent_pk])
        except:
            print("self.parent_pk or parent_reverse_prefix are not defined")
            url = super(ChildOwnerCreateView, self).get_success_url()
        finally:
            return url



class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        print('OwnerUpdateView:get_queryset called')
        
        qs = super(OwnerUpdateView, self).get_queryset()
        #qs <- Get the queryset of the model. of the object "pk" was
        
        return qs.filter(author = self.request.user)  # 'author' is from the DB model (Object).



class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    User's data.
    """

    def get_queryset(self):
        print('OwnerDeleteView:get_queryset called')
        
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(author = self.request.user)



# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid

# https://stackoverflow.com/questions/862522/django-populate-user-id-when-saving-a-model

# https://stackoverflow.com/a/15540149

# https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview


# Mine
# read:
# https://stackoverflow.com/questions/18172102/object-ownership-validation-in-django-updateview
# One can check it, like described in:
# https://stackoverflow.com/questions/28775123/edit-and-replay-xhr-chrome-firefox-etc
# Or in
# https://stackoverflow.com/q/4797534/3790620