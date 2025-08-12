from django.shortcuts import render
from .forms import PlantImageForm
from .ollama_utils import ask_ollama_with_image
import os
from django.conf import settings

def upload_image(request):
    result = None
    if request.method == "POST":
        form = PlantImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(path, "wb+") as dest:
                for chunk in image.chunks():
                    dest.write(chunk)

            # Send image to Ollama
            prompt = "What plant is this? Provide the common name and some details."
            result = ask_ollama_with_image(path, prompt)
    else:
        form = PlantImageForm()

    return render(request, "agent_view.html", {"form": form, "result": result})