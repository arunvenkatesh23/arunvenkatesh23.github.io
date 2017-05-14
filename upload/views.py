from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from .forms import FileForm, FolderForm
from .models import Folder, File

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_folder(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        form = FolderForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.folder_image = request.FILES['folder_image']
            file_type = folder.folder_image.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'folder': folder,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'upload/folder_form.html', context)
            folder.save()
            return render(request, 'upload/detail.html', {'folder': folder})
        context = {
            "form": form,
        }
        return render(request, 'upload/folder_form.html', context)


def create_file(request, folder_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        form = FileForm(request.POST or None, request.FILES or None)
        folder = get_object_or_404(Folder, pk=folder_id)
        if form.is_valid():
            folder_files = folder.file_set.all()
            for s in folder_files:
                if s.file_name == form.cleaned_data.get("file_name"):
                    context = {
                        'folder': folder,
                        'form': form,
                        'error_message': 'You already added that file',
                    }
                    return render(request, 'upload/file_form.html', context)
            file = form.save(commit=False)
            file.user = request.user
            file.folder = folder
            file.file = request.FILES['file']
            file_type = file.file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in AUDIO_FILE_TYPES:
                context = {
                    'folder': folder,
                    'form': form,
                    'error_message': 'Audio file must be WAV, MP3, or OGG',
                }
                return render(request, 'upload/file_form.html', context)

            file.save()
            return render(request, 'upload/detail.html', {'folder': folder})
        context = {
            'folder': folder,
            'form': form,
        }
        return render(request, 'upload/file_form.html', context)


def update_folder(request, folder_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        folder = get_object_or_404(Folder, pk=folder_id)
        if request.POST:
            form = FolderForm(request.POST or None, request.FILES or None, instance=folder)
            if form.is_valid():
                form.folder_image = request.FILES['folder_image']
                file_type = folder.folder_image.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    context = {
                        'folder': folder,
                        'form': form,
                        'error_message': 'Image file must be PNG, JPG, or JPEG',
                    }
                    return render(request, 'upload/update_folder.html', context)
                form.save()
                fold = Folder.objects.all()
                context = {
                    "folder": fold
                }
                return render(request, 'upload/index.html', context)
            else:
                folder = Folder.objects.get(pk=folder_id)
                form = FolderForm(request.POST, instance=folder)
                context = {
                    "form": form,
                }
                return render(request, 'upload/update_folder.html', context)


def delete_folder(request, folder_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        folder = get_object_or_404(Folder, pk=folder_id)
        folder.delete()
        fold = Folder.objects.all()
        return render(request, 'upload/index.html', {'folder': fold})


def delete_file(request, folder_id, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        folder = get_object_or_404(Folder, pk=folder_id)
        file = File.objects.get(pk=file_id)
        file.delete()
        return render(request, 'upload/detail.html', {'folder': folder})


def files_delete(request, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        file = File.objects.get(pk=file_id)
        file.delete()
        fil = File.objects.all()
        return render(request, 'upload/files.html', {'folder_all': fil})


def detail(request, folder_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        user = request.user
        folder = get_object_or_404(Folder, pk=folder_id)
        return render(request, 'upload/detail.html', {'folder': folder, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        folder = Folder.objects.filter(user=request.user)
        file_results = File.objects.all()
        query = request.GET.get("q")
        if query:
            folder = folder.filter(
                Q(folder_name__icontains=query)
            ).distinct()
            file_results = file_results.filter(
                Q(file_name__icontains=query)
            ).distinct()
            return render(request, 'upload/index.html', {
                'folder': folder,
                'files': file_results,
            })
        return render(request, 'upload/index.html', {'folder': folder})


def files(request, filter_by):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        try:
            file_ids = []
            for folder in Folder.objects.filter(user=request.user):
                for file in folder.file_set.all():
                    file_ids.append(file.pk)
            users_files = File.objects.filter(pk__in=file_ids)
            if filter_by == 'favorites':
                users_files = users_files.filter(is_favorite=True)
        except Folder.DoesNotExist:
            users_files = []
        context = {
            'folder_all': users_files,
            'filter_by': filter_by,
        }
        return render(request, 'upload/files.html', context)


def folders(request, filter_by):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        try:
            folder_ids = []
            for folder in Folder.objects.filter(user=request.user):
                folder_ids.append(folder.pk)
            users_folders = Folder.objects.filter(pk__in=folder_ids)
            if filter_by == 'favorites':
                users_folders = users_folders.filter(is_favorite=True)
        except Folder.DoesNotExist:
            users_folders = []
        context = {
            'folder': users_folders,
            'filter_by': filter_by,
        }
        return render(request, 'upload/folders.html', context)


def profile_settings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'upload/profile_settings.html')


def favorite_file(request, folder_id, file_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        file = get_object_or_404(File, pk=file_id)
        if file.is_favorite:
            file.is_favorite = False
        else:
            file.is_favorite = True
        file.save()
        user = request.user
        folder = get_object_or_404(Folder, pk=folder_id)
        return render(request, 'upload/detail.html', {'folder': folder, 'user': user})


def favorite_folder(request, folder_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        folder = get_object_or_404(Folder, pk=folder_id)
        if folder.is_favorite:
            folder.is_favorite = False
        else:
            folder.is_favorite = True
        folder.save()
        return HttpResponseRedirect('/app/folders/')
