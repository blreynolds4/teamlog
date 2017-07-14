from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.forms.models import model_to_dict
from tagging.models import Tag
from tagging.utils import edit_string_for_tags
from datetime import datetime, date

from .parsing import parse_duration
from .models import TeamPost, RunPost, PostComment


def parse_date(date_str):
    dt = datetime.strptime(date_str, settings.DATE_FORMAT)
    return dt.date()


def save_submitted_run_data(values, run_id):
    print("Saving values", values)
    result = dict()
    if run_id:
        result['id'] = run_id
    result['post_date'] = values.get('run_date', '')
    result['distance'] = values.get('run_distance', '')
    result['duration'] = values.get('run_time', '')
    result['route'] = values.get('run_route', '')
    result['message'] = values.get('run_description', '')
    result['details'] = values.get('run_details', '')

    return result


def save_submitted_msg_data(values, msg_id):
    result = dict()
    if msg_id:
        result['id'] = msg_id

    result['post_date'] = values.get('msg_date', '')
    result['message'] = values.get('message', '')

    return result


class DeleteView(LoginRequiredMixin, TemplateView):
    def post(self, request, post_id):
        post = TeamPost.objects.get(pk=post_id)
        # only allow deleting your own posts
        if post.author.user.id == request.user.id:
            print("Deleting post id", post_id)
            post.delete()
            print("Deleted post id", post_id)
        return redirect("home")


class RunView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_run.html"

    def get(self, request, post_id=None):
        run = dict()
        run['post_date'] = date.today().strftime(settings.DATE_FORMAT)
        run['duration'] = None
        run['post_target'] = 'posts:new_run'

        if post_id:
            temp = RunPost.objects.get(pk=post_id)
            run = model_to_dict(temp)
            run['post_date'] = temp.post_date.strftime(settings.DATE_FORMAT)
            run['duration'] = temp.display_time()
            run['post_target'] = 'posts:edit_run'

        return render(request, 'posts/edit_run.html', dict(run=run))

    def post(self, request, post_id=None):
        '''
        Handle creates and edits of runs
        If there is an error in the date, time, or distance
        we need to render the correct
        '''
        print("Saving run with id", post_id)
        run = save_submitted_run_data(request.POST, post_id)
        run['post_target'] = 'posts:edit_run' if post_id else 'posts:new_run'
        try:
            post_date = parse_date(request.POST['run_date'])

            if request.POST['run_distance'] and request.POST['run_time']:
                if not post_id:
                    new_run = RunPost(author=request.user.userprofile,
                                      duration=parse_duration(request.POST['run_time']),
                                      distance=float(request.POST['run_distance']),
                                      message=request.POST['run_description'],
                                      route=request.POST['run_route'],
                                      details=request.POST['run_details'],
                                      post_date=post_date)
                    new_run.save()
                    print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
                    Tag.objects.update_tags(new_run.teampost_ptr, edit_string_for_tags(request.user.userprofile.tags))
                else:
                    r = RunPost.objects.get(pk=post_id)
                    r.duration = parse_duration(request.POST['run_time'])
                    r.distance = float(request.POST['run_distance'])
                    r.message = request.POST['run_description']
                    r.route = request.POST['run_route']
                    r.details = request.POST['run_details']
                    r.post_date = post_date
                    r.save()

                return redirect("home")
            else:
                print("Rending template with run", run)
                return render(request,
                              self.template_name,
                              dict(error="Run requires at least time and distance.", run=run))
        except ValueError:
            return render(request,
                          self.template_name,
                          dict(error="Date format must be 01-01-2017 (leading zeroes required)", run=run))


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = "posts/edit_msg.html"

    def get(self, request, msg_id=None):
        msg = dict()
        msg['post_date'] = date.today().strftime(settings.DATE_FORMAT)
        msg['post_target'] = 'posts:new_msg'

        if msg_id:
            temp = TeamPost.objects.get(pk=msg_id)
            msg = model_to_dict(temp)
            msg['post_date'] = temp.post_date.strftime(settings.DATE_FORMAT)
            msg['post_target'] = 'posts:edit_msg'

        print("GET MSG", msg)
        return render(request, 'posts/edit_msg.html', dict(msg=msg))

    def post(self, request, msg_id=None):
        msg = save_submitted_msg_data(request.POST, msg_id)
        msg['post_target'] = 'posts:edit_msg' if msg_id else 'posts:new_msg'
        try:
            post_date = parse_date(request.POST['msg_date'])
            if request.POST['message']:
                if msg_id is None:
                    m = TeamPost(author=request.user.userprofile,
                                 message=request.POST['message'],
                                 post_date=post_date)
                    m.save()
                    print("User", request.user.username, "Tags", edit_string_for_tags(request.user.userprofile.tags))
                    Tag.objects.update_tags(m, edit_string_for_tags(request.user.userprofile.tags))
                else:
                    m = TeamPost.objects.get(pk=msg_id)
                    m.message = request.POST['message']
                    m.post_date = post_date
                    m.save()

                return redirect("home")
            else:
                return render(request,
                              self.template_name,
                              dict(error="Message is required.", msg=msg))
        except ValueError:
            return render(request,
                          self.template_name,
                          dict(error="Date format must be 01-01-2017 (leading zeroes required)",
                               msg=msg))


class CommentView(LoginRequiredMixin, TemplateView):
    template_name = "posts/comment.html"

    def get(self, request, msg_id=None):
        '''
        This can be either a get to create a comment or a get
        to edit a comment.
        In the create case the msg id is set and comment is none.
        In the edit case hopefully the msg can be none and the comment id can be set.
        '''
        comment = dict()
        comment['post_target'] = 'posts:new_comment'
        comment['message_id'] = msg_id
        return render(request, self.template_name, dict(comment=comment))

    def post(self, request, msg_id):
        print("Creating new comment")
        msg = TeamPost.objects.get(pk=msg_id)
        comment = PostComment(author=request.user.userprofile,
                              comment=request.POST['comment'],
                              original_post=msg)
        comment.save()
        return redirect("home")


class CommentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = "posts/comment.html"

    def post(self, request, comment_id):
        comment = PostComment.objects.get(pk=comment_id)
        comment.delete()
        return redirect("home")
