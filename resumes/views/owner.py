from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """


class OwnerDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """


class ParentOwnerDetailView(OwnerDetailView):
    """
    Sub-class of OwnerDetailView, that designed for handling a model with
    child model in the context_data.
    Parent view with its child model form, in the context.
    """
    child_model = None
    child_form = None

    def get_context_data(self, **kwargs):
        context = super(ParentOwnerDetailView, self).get_context_data(**kwargs)

        # Getting the specific Parent Item
        pk = self.kwargs['pk']
        ParentQuery = get_object_or_404(self.model, id=pk)

        # Get all the existing Childs of the Parent
        qQuery = Q(**{f'{self.model._meta.verbose_name}': ParentQuery})
        childs = self.child_model.objects.filter(qQuery).order_by("-updated_at")

        # define context names
        parent_model_name = f'{self.model.__name__.lower()}'
        childs_plural_name = f'{self.child_model._meta.verbose_name_plural}'
        child_form_verbose_name = f'{self.child_model._meta.verbose_name}_form'
        # init the child form
        child_form_empty_init = self.child_form()

        context = {
            f'{parent_model_name}': ParentQuery,
            f'{childs_plural_name}': childs,
            f'{child_form_verbose_name}': child_form_empty_init}

        return context


class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # https://stackoverflow.com/questions/21652073/django-how-to-set-a-hidden-field-on-a-generic-create-view
    # https://stackoverflow.com/questions/19051830/a-better-way-of-setting-values-in-createview
    def form_valid(self, form):
        # print('OwnerCreateView:form_valid called')
        form.instance.author = self.request.user

        return super(OwnerCreateView, self).form_valid(form)


class ParentOwnerCreateView(OwnerCreateView):
    """
    Sub-class of the OwnerCreateView, that redirect to its own detailview(?)
    """
    pass


class ChildOwnerCreateView(OwnerCreateView):
    """
    Sub-class of OwnerCreateView, that abstract the logic of creating an
    object from the parent page/view.
    Associate the child item with correct parent pk.
    """

    # new class attributes, for parent association.
    parent_model = None
    parent_reverse_prefix = None
    parent_pk = None

    # override the 'form_valid' method
    def form_valid(self, form):
        try:
            self.parent_pk = self.kwargs.get('pk', None)
            currentParent = get_object_or_404(self.parent_model, id=self.parent_pk)

            # find the field from the type of the parent and popluate it
            setattr(form.instance, self.parent_model.__name__.lower(), currentParent)
        except Exception as e:
            print("ChildOwnerCreateView:form_valid:Exception:\n", e, type(e))

        return super(ChildOwnerCreateView, self).form_valid(form)

    # override the 'get_success_url' method
    def get_success_url(self):
        try:
            url = reverse(self.parent_reverse_prefix, args=[self.parent_pk])
        except Exception as e:
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
        # print('OwnerUpdateView:get_queryset called')

        qs = super(OwnerUpdateView, self).get_queryset()
        # qs <- Get the queryset of the model. 
        # QuerySet of all objects from the model, but it is filtered in 'get_object', using 'pk'.
        # The QuerySet is executed in 'get_object', using 'get' method (for one object only)

        return qs.filter(author=self.request.user)  # filter on 'author'.


class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    User's data.
    """

    def get_queryset(self):
        # print('OwnerDeleteView:get_queryset called')

        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(author=self.request.user)



# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ModelFormMixin.form_valid

# https://stackoverflow.com/questions/862522/django-populate-user-id-when-saving-a-model

# https://stackoverflow.com/a/15540149

# https://stackoverflow.com/questions/5531258/example-of-django-class-based-deleteview


# template names in:
# https://docs.djangoproject.com/en/3.1/topics/auth/default/#module-django.contrib.auth.views


# Mine
# read:
# https://stackoverflow.com/questions/18172102/object-ownership-validation-in-django-updateview
# One can check it, like described in:
# https://stackoverflow.com/questions/28775123/edit-and-replay-xhr-chrome-firefox-etc
# Or in
# https://stackoverflow.com/q/4797534/3790620
