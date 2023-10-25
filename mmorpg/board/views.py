from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from .models import Post, Response, User
from .forms import PostForm, ResponseForm
from .filters import ResponseFilter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta



def WelcomeView(request):
    return render(request, template_name="board/Welcome.html")

@login_required
def Accepted(request):
    response_id = request.GET['response_id']
    response_to_accept = Response.objects.get(pk=response_id)
    response_to_accept.accepted = True
    response_to_accept.save()

    link = f"http://127.0.0.1:8000/board/private/responseview/?response_id={str(response_id)}"
    user = User.objects.get(pk=response_to_accept.responseUser.pk)

    html_content = render_to_string('board/accept_response_send.html',
                                    {'response': response_to_accept, "user": user, "link": link, })

    msg = EmailMultiAlternatives(
        subject=f'Принят отклик к объявлению с заголовком:{response_to_accept.responsePost.title} от {response_to_accept.responsePost.postUser}',
        body=response_to_accept.text,
        from_email='bulanov-rvp@yandex.ru',
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    print("Отправляю письмо", user.email)
    msg.send()

    return render(request, template_name="board/accepted.html", context={'response_to_accept':response_to_accept})

@login_required
def Unaccepted(request):
    response_id = request.GET['response_id']
    response_to_unaccept = Response.objects.get(pk=response_id)
    response_to_unaccept.accepted = False
    response_to_unaccept.save()
    return render(request, template_name="board/unaccepted.html", context={'response_to_unaccept':response_to_unaccept})

@login_required
def Responseview(request):
    response_id = request.GET['response_id']
    response = Response.objects.get(pk=response_id)
    return render(request, template_name="board/responseview.html", context={'response':response})

def weekly_emailing():
    day = datetime.now() - timedelta(days=7)
    week_posts = Post.objects.filter(date__gt = day)
    all_users = User.objects.all()

    if week_posts:
        for user in all_users:
            html_content = render_to_string('board/post_weekly_emailing.html', {'posts':week_posts , "user": user, })

            msg = EmailMultiAlternatives(
                    subject=f'Список объявлений за неделю',
                    body="",
                    from_email='bulanov-rvp@yandex.ru',
                    to=[user.email],
                )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Письмо отправлено", user.email)


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'board/response_delete.html'
    queryset = Response.objects.all()
    success_url = '/board/private/'

class PrivateTemplateView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/private_page.html'
    context_object_name = 'response_all'
    queryset = Response.objects.order_by("text")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_objs'] = Response.objects.filter(responsePost__postUser__id=self.request.user.id)
        context['filter'] = ResponseFilter(self.request.GET, queryset=self.get_queryset())
        return context

class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'board/post_all.html'
    context_object_name = 'post_all'
    # это имя списка, в котором будут лежать все объекты, его надо указать,
    # чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by("-date" )
#     # # paginate_by = 7
#

class PostDetail(DetailView):
    pass
    model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'board/post_detail.html' # название шаблона будет product.html
    context_object_name = 'post_detail' # название объекта
#     # queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'board/post_create.html'
    form_class = PostForm
    # permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):

        post = Post(
            category = request.POST['category'],
            title = request.POST['title'],
            postUser_id = request.POST['postUser'],
            text=request.POST['text'],
        )
        post.save()

        return render(request, template_name='board/post_detail.html', context={'post_detail': post, })


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'board/post_create.html'
    form_class = PostForm
    # permission_required = ('news.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'board/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/board/'

class ResponseCreateView(LoginRequiredMixin, CreateView):
    # model = Response
    template_name = 'board/response_create.html'
    form_class = ResponseForm
    # permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_obj'] = Post.objects.get(pk=self.request.GET['post_id'])
        return context

    def post(self, request, *args, **kwargs):
        response = Response(
            responsePost_id = self.request.GET['post_id'],
            responseUser_id = self.request.user.pk,
            text=request.POST['text'],
        )
        response.save()

        return render(request, template_name='board/response_detail.html', context={'response': response, })